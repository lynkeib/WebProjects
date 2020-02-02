/*
Todo List
- "new" - Add a todo
- "list" - View all todos
- "quit" - Quit App
*/
var command = null;
var todo = [];
while(command !== "quit"){
    command = prompt("What would you like to do?");
    if(command === "new"){
        todo.push(prompt("Enter a new todo"));
    }
    else if(command === "list") {
        console.log(todo);
    }
    else {
        continue;
    }
};