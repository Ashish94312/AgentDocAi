import subprocess
import json
import os
import markdown
import asyncio
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from langchain_openai import ChatOpenAI

from .crews.crew import build_crew, execute_crew_async

GITHUB_TOKEN = getattr(settings, 'GITHUB_PERSONAL_ACCESS_TOKEN', None)
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
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                markdown_content = ""
                # handle markdown code blocks
                if lines and lines[0].strip() == "```markdown" and len(lines) > 1 and lines[-1].strip() == "```":
                    markdown_content = "".join(lines[1:-1]).strip()
                else:
                    markdown_content = "".join(lines).strip()
                combined_content += f"\n\n---\n\n" + markdown_content
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
    
    try:
        with open(output_path, "w") as f:
            f.write(combined_content.strip())
        print(f"Combined output saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving combined markdown: {e}")
        return None

def convert_markdown_to_html(markdown_file_path):
    try:
        with open(markdown_file_path, "r") as f:
            markdown_text = f.read()
            html_content = markdown.markdown(markdown_text, extensions=['extra'])
            return html_content
    except FileNotFoundError:
        print(f"Error: Markdown file not found at {markdown_file_path}")
        return None
    except Exception as e:
        print(f"Error converting Markdown to HTML: {e}")
        return None


def documentation_interface(request):
    return render(request, 'mcp_manager/documentation_interface.html')


def generate_documentation(request):
    if request.method == 'POST':
        repo_url = request.POST.get('repo_url', '')
        if repo_url:
            try:
                owner, repo_name = extract_owner_repo(repo_url)

                if owner and repo_name:
                    if not OPENAI_API_KEY:
                        error = "Error: OPENAI_API_KEY is not set in Django settings."
                        return render(request, 'mcp_manager/documentation_interface.html', {'error': error})

                    # TODO: make this configurable
                    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo-16k")

                    crew = build_crew(owner, repo_name)
                    crew.kickoff()

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
                            return render(request, 'mcp_manager/documentation_display.html', {
                                'documentation': html_content
                            })
                        else:
                            error = "Failed to convert combined Markdown to HTML."
                            return render(request, 'mcp_manager/documentation_interface.html', {'error': error})
                    else:
                        error = "Failed to combine the documentation files."
                        return render(request, 'mcp_manager/documentation_interface.html', {'error': error})
                else:
                    error = "Invalid GitHub repository URL."
                    return render(request, 'mcp_manager/documentation_interface.html', {'error': error})

            except ValueError as e:
                error = str(e)
                return render(request, 'mcp_manager/documentation_interface.html', {'error': error})

    return render(request, 'mcp_manager/documentation_interface.html')


async def generate_documentation_async(request):
    if request.method == 'POST':
        repo_url = request.POST.get('repo_url', '')
        if repo_url:
            try:
                owner, repo_name = extract_owner_repo(repo_url)

                if owner and repo_name:
                    if not OPENAI_API_KEY:
                        error = "Error: OPENAI_API_KEY is not set in Django settings."
                        return render(request, 'mcp_manager/documentation_interface.html', {'error': error})

                    print(f"Starting async documentation generation for {owner}/{repo_name}")
                    crew_result = await execute_crew_async(owner, repo_name)
                    print(f"Async crew execution completed for {owner}/{repo_name}")

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
                            return render(request, 'mcp_manager/documentation_display.html', {
                                'documentation': html_content
                            })
                        else:
                            error = "Failed to convert combined Markdown to HTML."
                            return render(request, 'mcp_manager/documentation_interface.html', {'error': error})
                    else:
                        error = "Failed to combine the documentation files."
                        return render(request, 'mcp_manager/documentation_interface.html', {'error': error})
                else:
                    error = "Invalid GitHub repository URL."
                    return render(request, 'mcp_manager/documentation_interface.html', {'error': error})

            except ValueError as e:
                error = str(e)
                return render(request, 'mcp_manager/documentation_interface.html', {'error': error})

    return render(request, 'mcp_manager/documentation_interface.html')


@csrf_exempt
@require_http_methods(["POST"])
async def generate_documentation_api_async(request):
    try:
        data = json.loads(request.body)
        repo_url = data.get('repo_url', '')
        
        if not repo_url:
            return JsonResponse({'error': 'Repository URL is required'}, status=400)
        
        owner, repo_name = extract_owner_repo(repo_url)
        
        if not OPENAI_API_KEY:
            return JsonResponse({'error': 'OPENAI_API_KEY is not set in Django settings'}, status=500)
        
        print(f"Starting async API documentation generation for {owner}/{repo_name}")
        crew_result = await execute_crew_async(owner, repo_name)
        print(f"Async API crew execution completed for {owner}/{repo_name}")
        
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
                return JsonResponse({
                    'success': True,
                    'documentation': html_content,
                    'owner': owner,
                    'repo': repo_name
                })
            else:
                return JsonResponse({'error': 'Failed to convert Markdown to HTML'}, status=500)
        else:
            return JsonResponse({'error': 'Failed to combine documentation files'}, status=500)
            
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)