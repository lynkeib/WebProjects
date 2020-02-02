/*
Todo List
- "new" - Add a todo
- "list" - View all todos
- "quit" - Quit App
- "delete" - Remove a todo
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
    else if (command === "delete"){
        var remove_index = prompt("Enter index of todo to delete")
        if(remove_index < 0 || remove_index >= todo.length){
            console.log("No such index");
            continue;
        }
        else{
            todo.splice(remove_index);
        }
    }
    else {
        break;
    }
};