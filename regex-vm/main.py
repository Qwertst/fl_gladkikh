from src.regex import RegexMachine

VM = RegexMachine("a+b?|c*")
VM.print()
print(VM.accepts(""))
