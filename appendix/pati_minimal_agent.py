from typing import Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.globals import set_debug
set_debug(True)

# -----------------------------
# 1. Tool definitions
# -----------------------------

def delete_file(path: str, user_permission_level: int):
    required = 3
    if user_permission_level < required:
        return "Permission denied"
    return f"[Simulated] Deleted file: {path}"

TOOLS = {
    "delete_file": delete_file,
}

TOOL_SPECS = {
    "delete_file": {
        "required_permission_level": 3,
        "args": ["path"]
    }
}

# -----------------------------
# 2. Permission-Aware ReAct Agent
# -----------------------------

class PermissionAwareReActAgent:
    def __init__(self, llm: ChatOllama, tools, tool_specs, user_permission_level: int):
        self.llm = llm
        self.tools = tools
        self.tool_specs = tool_specs
        self.user_permission_level = user_permission_level

    def run(self, user_input: str):
        prompt = self._build_prompt(user_input)
        llm_output = self.llm.invoke(prompt)

        # AIMessage → string
        llm_text = llm_output.content
        print("LLM Output:", llm_text)

        tool_name, args = self._parse_tool_call(llm_text)
        if tool_name is None:
            return f"LLM Response: {llm_text}"

        # Permission Injection
        args["user_permission_level"] = self.user_permission_level

        return self._execute_tool(tool_name, args)

    # -----------------------------
    # Prompt construction
    # -----------------------------

    def _build_prompt(self, user_input: str) -> str:
        tool_desc = "\n".join(
            f"- {name}: args={spec['args']}"
            for name, spec in self.tool_specs.items()
        )

        return f"""
            You are a ReAct agent.

            When you decide to use a tool, you MUST output ONLY a Python-style function call:

                delete_file(path="foo.txt")

            Rules:
            - Output ONLY the function call.
            - Do NOT output explanations.
            - Do NOT wrap the tool name.
            - Do NOT invent new syntax.

            Available tools:
            {tool_desc}

            User input: {user_input}

            Think step-by-step, then output ONLY the tool call.
            """

    # -----------------------------
    # Tool call parsing
    # -----------------------------

    def _parse_tool_call(self, text: str):
        if "(" not in text or ")" not in text:
            return None, {}

        try:
            name = text.split("(")[0].strip()
            arg_str = text.split("(")[1].split(")")[0]

            args = {}
            for pair in arg_str.split(","):
                if "=" in pair:
                    k, v = pair.split("=")
                    args[k.strip()] = v.strip().strip('"')

            return name, args

        except Exception:
            return None, {}

    # -----------------------------
    # Tool execution
    # -----------------------------

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]):
        if tool_name not in self.tools:
            return f"Unknown tool: {tool_name}"

        tool = self.tools[tool_name]
        return tool(**args)



def main():
    print("Hello from pati!")

    # -----------------------------
    # 3. Instantiate the agent
    # -----------------------------

    llm = ChatOllama(model="qwen3:1.7b")

    agent = PermissionAwareReActAgent(
        llm=llm,
        tools=TOOLS,
        tool_specs=TOOL_SPECS,
        user_permission_level=2
    )

    # -----------------------------
    # 4. Run
    # -----------------------------

    print(agent.run("Delete the file foo.txt"))



if __name__ == "__main__":
    main()
