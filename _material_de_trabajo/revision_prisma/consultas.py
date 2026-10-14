BASE = 'from_publication_date:2022-01-01,to_publication_date:2026-09-30'
CIBER = '(cybersecurity OR "cyber security" OR "cyber defense" OR "cyber defence" OR "cyber-attack" OR "penetration testing" OR "security operations" OR "offensive security")'
A_TIT = '(agent OR agents OR agentic OR "multi-agent")'
A_ABS = '("large language model" OR "large language models" OR LLM OR LLMs OR "language model" OR "reinforcement learning" OR "agentic AI")'
B_TIT = '(education OR educational OR teaching OR course OR students OR curriculum OR training OR "capture the flag" OR CTF OR learning)'
B_ABS = '("large language model" OR "large language models" OR LLM OR LLMs OR "generative AI" OR ChatGPT OR "AI agent" OR "AI agents" OR agentic)'
OPENALEX = {
    'A': f'{BASE},title.search:{A_TIT} AND {CIBER},title_and_abstract.search:{A_ABS}',
    'B': f'{BASE},title.search:{CIBER} AND {B_TIT},title_and_abstract.search:{B_ABS}',
}
# arXiv (sintaxis propia: ti = título, abs = resumen)
AX_CIBER = '(ti:cybersecurity OR ti:"cyber security" OR ti:"cyber defense" OR ti:"cyber defence" OR ti:"penetration testing" OR ti:"security operations" OR ti:"offensive security")'
ARXIV = {
    'A': f'(ti:agent OR ti:agents OR ti:agentic OR ti:"multi-agent") AND {AX_CIBER} AND (abs:"large language model" OR abs:LLM OR abs:"language model" OR abs:"reinforcement learning" OR abs:agentic)',
    'B': f'{AX_CIBER} AND (ti:education OR ti:educational OR ti:teaching OR ti:course OR ti:students OR ti:curriculum OR ti:training OR ti:"capture the flag" OR ti:CTF OR ti:learning) AND (abs:"large language model" OR abs:LLM OR abs:"generative AI" OR abs:ChatGPT OR abs:"AI agent" OR abs:agentic)',
}
