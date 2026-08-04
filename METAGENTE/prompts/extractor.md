Your task is to shorten and extract only the introduction and description information from a technical project. You are given the following technical text from a project:
<README>
$readme_text
</README>
 
# Steps
- **Identify the structure of the repository**: The file is a structure text file that might contains many sections such as introduction, description, installation, contributing, license,...
- **Remove all sections that are not relevant to the introduction or description of the repository**: Irrelevant sections might include technical guidance (installing/running/specification... instruction), repository structure/table of contents, contributions/references,...
- **Remove all unnecessary links/tags**: Identify all links/tags that DO NOT contribute to the description of the repository. You must remove all of these reference links and tags.
- **Return only text that is relevant to the description of the repository**: The output should only contains the text that is relevant to the introduction/description of the repository, including the project name/title, project tagline/functional description/purpose statement/overview. DO NOT include any output identifications such as: "Here's the ..." or "Extracted text:"
