# Mode types:
# 'r' = read (default)
# 'w' = write (if already exist will overwrite existing)
# 'r+'= read and write
# 'x' = write (if already exist will give error, use to create new file)
# 'a' = write (append to end of file if exist)
# 'b' = open in binary mode (Note: to use together with 'w' 'r' etc. Example 'wb')

## Creating or overwriting file
# f = open('demo.txt', mode='w')
# f.write("Hello Python!")
# f.close

## read whole file
f = open('demo.txt', mode='r')
file_content = f.read()
f.close()
print(file_content)

## read file line per line (returns a List, one entry per line)
## Note, the returned elements contain the \n new line caracter treated as 1 character
f = open('demo.txt', mode='r')
file_content = f.readlines()
f.close()
print(file_content)
for line in file_content:
## The -1 range selector removes the line break
    print(line[:-1])

## With readline we read only one line of the file
f = open('demo.txt', mode='r')
line = f.readline()
while line:
    print(line)
    line = f.readline()
f.close()

#### !!!Opening and closing files can be managed by Python with the 
#### with open as function note it ends with : then indentetion.
#### when code goes out of indentation the file is closed automatically
#### No need to closing file
with open('demo.txt', mode='r') as f:
    line = f.readline()
    while line:
        print(line)
        line = f.readline()
print("Done!")

## Appending to existing file
# f = open('demo.txt', mode='a')
# # \n gives a new line
# f.write("This is added text on new line\n")
# f.close()

