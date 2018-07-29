import commands
import types

# print(commands.__dict__)
def show_commands():
  command_list = ['__Commands:__']
  ignore_imports = ['random', 'requests', 'pdb', 'json', 'add_point', 'flip_coin', 'find_player', 'items', 'buy_item', 'attack_enemy']
  for name, command in commands.__dict__.items():
      valid_name = name not in ignore_imports and '__' not in name
      not_built_in = isinstance(command, types.BuiltinFunctionType) is False
      is_function = isinstance(command, types.FunctionType)

      if not_built_in and valid_name and is_function:
          description = command.__doc__
          command_list.append(f"`**{name.upper()}**: {description}`")

  message = '\n'.join(command_list)
  print(message)
  return message