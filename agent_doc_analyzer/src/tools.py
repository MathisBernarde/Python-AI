"""
Tool definitions (Calculator, Currency Fetcher, File Reader).
"""
class BaseTool:
    def execute(self, *args, **kwargs):
        raise NotImplementedError
