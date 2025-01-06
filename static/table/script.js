async function remove_object(object){
    //event.preventDefault();    // prevent page from refreshing
    let response = await fetch("/remove", {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json'
           },
            body: JSON.stringify(object)
        });
    location.reload();
}

async function add_object(object){
    //event.preventDefault();    // prevent page from refreshing
    let response = await fetch("/add", {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json'
           },
            body: JSON.stringify(object)
        });
    location.reload();
}
