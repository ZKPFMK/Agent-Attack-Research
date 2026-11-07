"""agentattack -- evaluation library and multi-agent testbed for research on attacks against LLM agents.

Modules: metrics (ASR + Wilson/bootstrap CIs, McNemar), judge (kappa, judge-vs-gold report),
threat_model (structured threat model + checks), kb (parse/search the user's knowledge base),
llm (mock / OpenAI-compatible / cached backends), mas (propagation testbed), runner (resumable
trial grids), toy (rule-based stand-in agents; TOY, not a model of any real LLM), cli (``aa``).
"""
__version__ = "0.1.0"
