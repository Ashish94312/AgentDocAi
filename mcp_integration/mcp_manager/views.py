import json
import os
import markdown
import asyncio
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .crews.crew import execute_crew_async

OPENAI_API_KEY = getattr(settings, 'OPENAI_API_KEY', None)

def extract_owner_repo(repo_url):
    parts = repo_url.split('/')
    if len(parts) >= 5 and parts[2] == 'github.com':
        owner = parts[3]
        repo_name = parts[4].replace('.git', '')
        return owner, repo_name
    else:
        raise ValueError("Invalid GitHub repository URL format.")

def combine_markdown_files(file_paths, output_path, owner, repo_name):
    combined_content = f"# Summary for {owner}/{repo_name}\n\n"
    for file_path in file_paths:
        with open(file_path, "r") as f:
            lines = f.readlines()
            markdown_content = ""
            # handle markdown code blocks
            if lines and lines[0].strip() == "```markdown" and len(lines) > 1 and lines[-1].strip() == "```":
                markdown_content = "".join(lines[1:-1]).strip()
            else:
                markdown_content = "".join(lines).strip()
            combined_content += f"\n\n---\n\n" + markdown_content
    
    with open(output_path, "w") as f:
        f.write(combined_content.strip())
    return output_path

def convert_markdown_to_html(markdown_file_path):
    
    with open(markdown_file_path, "r") as f:
        markdown_text = f.read()
        html_content = markdown.markdown(markdown_text, extensions=['extra'])
        return html_content


def documentation_interface(request):
    return render(request, 'mcp_manager/documentation_interface.html')


@csrf_exempt
@require_http_methods(["POST"])
def generate_documentation_api_async(request):
    data = json.loads(request.body)
    repo_url = data.get('repo_url', '')
    
    if not repo_url:
        return JsonResponse({'error': 'Repository URL is required'}, status=400)
    
    owner, repo_name = extract_owner_repo(repo_url)
    
    if not OPENAI_API_KEY:
        return JsonResponse({'error': 'OPENAI_API_KEY is not set in Django settings'}, status=500)
    
    crew_result = asyncio.run(execute_crew_async(owner, repo_name))
    
    # Create the generate_docs directory if it doesn't exist
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generate_docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    output_files = [
        os.path.join(docs_dir, "repo_structure.md"),
        os.path.join(docs_dir, "report_issues.md"),
        os.path.join(docs_dir, "pull_requests.md"),
        os.path.join(docs_dir, "branches.md")
    ]
    
    final_output_path = os.path.join(docs_dir, "summary.md")
    combined_markdown_path = combine_markdown_files(output_files, final_output_path, owner, repo_name)
    
    if combined_markdown_path:
        html_content = convert_markdown_to_html(combined_markdown_path)
        if html_content:
            return JsonResponse({'success': True, 'documentation': html_content, 'owner': owner, 'repo': repo_name})
        else:
            return JsonResponse({'error': 'Failed to convert Markdown to HTML'}, status=500)
    else:
        return JsonResponse({'error': 'Failed to combine documentation files'}, status=500)