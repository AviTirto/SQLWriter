import os
import dotenv
from composio_langchain import App, ComposioToolSet, Action
from crewai import Agent, Crew, Process, Task
from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv()

toolset = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])
# tool_set = ComposioToolSet()
# code_interpreter_tools = tool_set.get_actions(actions=[Action.CODEINTERPRETER_EXECUTE_CODE])
code_interpreter_tools = toolset.get_tools([App.CODEINTERPRETER])
# tools = tool_set.get_actions(actions=[Action.CODEINTERPRETER_EXECUTE_CODE])
# code_interpreter_tools = [toolset.get_actions(actions=[Action.CODEINTERPRETER_EXECUTE_CODE]), toolset.get_actions(actions=[Action.CODEINTERPRETER_RUN_TERMINAL_CMD]), toolset.get_actions(actions=[Action.CODEINTERPRETER_GET_FILE_CMD])]
sql_tools = toolset.get_tools([App.SQLTOOL])

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                             api_key=os.environ['GOOGLE_API_KEY']
                          ) 

while True:
    main_task = input("Enter the task you want to perform (or type 'exit' to quit): ")
    if main_task.lower() == "exit":
        break
        
    code_interpreter_agent = Agent(
        role="Python Code Interpreter Agent",
        goal="Run a code to get achieve a task given by the user",
        backstory="You are an agent that helps users run Python code.",
        verbose=True,
        tools=code_interpreter_tools,
        llm=llm,
        max_rpm=5
    )
    
    sql_agent = Agent(
        role="SQL Agent",
        goal="Run SQL queries to get achieve a task given by the user",
        backstory=(
            "You are an agent that helps users run SQL queries. "
            "Connect to the local SQLite DB at connection string = company.db"
            "Try to analyze the tables first by listing all the tables and columns "
            "and doing distinct values for each column and once sure, make a query to \
            get the data you need."
        ),
        verbose=True,
        tools=sql_tools,
        llm=llm,
        allow_delegation=True,
        max_rpm=5
    )
    
    code_interpreter_task = Task(
        description=f"Run Python code to achieve the task - {main_task}. \
        Exit once the image has been created.",
        expected_output="Python code executed successfully. Return the image path.",
        agent=code_interpreter_agent,
    )
    
    sql_task = Task(
        description=f"Run SQL queries to achieve a task - {main_task}",
        expected_output=f"SQL queries executed successfully. The result of the task \
        is returned - {main_task}",
        agent=sql_agent,
    )


    crew = Crew(
        agents=[sql_agent, code_interpreter_agent],
        tasks=[sql_task, code_interpreter_task],
    )

    result = crew.kickoff()
    print(result)

