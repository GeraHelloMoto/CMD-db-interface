import sqlite3
import sys

conn = sqlite3.connect('enterprise_db')
cur = conn.cursor()

# ///////Adding new value////////////////////
def add_manager():
	first_name = input('first name please: ')
	last_name = input('last name please: ')
	age = int(input('age please: '))
	product = input('product please: ')
	salary = int(input('salary please: '))
	with conn:  ## using a context manager u dont need to commit a command
		cur.execute('INSERT INTO office  VALUES (?,?,?,?,?)',(first_name,last_name,age,product,salary)) 
	conn.commit()

# ///////////Show whole table////////////
def show_all():
	query_list = list(cur.execute('Select * from office'))
	for query in query_list:
		print(query)
	conn.commit()

# ////////////Changing  value///////////////
def change():
	collumn = input('what collumn you want to change?')
	collumn_value = input('what value you want to change?')
	check_collumn = input('what collumn you want to use as check?')
	check_value = input('what value you want to use as check?')
	with conn: # changing name if age is equal
		cur.execute(f'update office set {collumn}=? where {check_collumn}=?',(collumn_value,check_value))

#////show some collumns////

def show_some():
	collumns_list = input ('what collumn you want to see?\n')
	with conn:
		if len(list(collumns_list))>1:
			params_list = list(collumns_list.split())
			res =''
			for item in params_list:
				res+=item+', '
			new_res = res.removesuffix(', ')
			new_command = 'select ' + new_res + ' from office'
		for i in cur.execute(new_command):
			print(i)

# /////////Deleting with args (1st is col_name 2nd is value)///////////
def delete():
	print(sys.argv)
	collumn = input('from what collumn')
	value = input('and the value you want to delete')
	with conn:
		cur.execute(f'delete from office where {collumn}=?',(value,))
	
# ///////Order by sth/////////
def order():
	what = input('what do you want to sort?')
	how = input('how do you want to sort it?')
	method = input('asc or desc?')
	with conn:
		for i in (list(cur.execute(f'select {what} from class order by {how} {method}'))):
			print(i)

# //////Your own command///////////
def my_command():
	command = input('tell me what to do: ')
	with conn:  ## execute user's command
		res = list(cur.execute(command))
		for i in res:
			print(i)
# my_command()		
def hints():
	some_hints = '''This is a short hint list for built-in functions:

add-manager ('INSERT INTO office  VALUES (collumns names)',(first_name,last_name,age,product,salary))'
show_all    ('Select * from office')
show_some   ('select ' + chosen values + ' from office')
order       ('select {what} from class order by {how} {method}')
change      ('update office set {collumn}=? where {check_collumn}=?',(collumn_value,check_value))
delete      ('delete from office where {collumn}=?',(value,))
my_command  (any sql command)
////////
default table name == office
collumns names for office table (name, surname, age, product, salary)
'''
	print(some_hints)
func_dict = {'add_manager':add_manager,'show_all':show_all,
'change':change,'delete':delete,'order':order,
'my_command':my_command,'show_some':show_some,'help':hints}
print('///////////////////////////////////////////')
print('######___WELCOME TO SQL INTERFACE___######')
print('///////////////////////////////////////////')
print('###__You can choose one of these commands:__##')
print('////////////////////////////////////////////')
print('#######__add_manager,show_all,show_some__########')
print('######__delete,change,order,my_command__######')
print('##############################################')
print('/////////////////////////////////////////////')
print('###__Or you can write you own sql request__###')
print('/////////////////////////////////////////////')
print('########___Type "help" to see hints___#########')
print('/////////////////////////////////////////////')


command = input('what do you want me to do for you?\n')
while command!='exit':
	try:
		if command in func_dict:
			
			func_dict[command]()
			command = input('what do you want me to do for you?\n')
		else:	
			with conn:
				print(list(cur.execute(command)))
				pass
			
			command = input('what do you want me to do for you?\n')	
	except:
		print('unknown command!')
		command = input('what do you want me to do for you?\n')		
print('Goodbye!')
exit()
