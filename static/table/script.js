function clearContents(element) {
  element.value = '';
}


async function remove_object(object){
    //event.preventDefault();    // prevent page from refreshing
    console.log(JSON.stringify([elemId,number]))
    const root = object.parentElement.parentElement
    const elemId = root.getAttribute("element")
    var number = root.getElementById("remove").value
    let response = await fetch("/remove", {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json'
           },
            body: JSON.stringify([elemId,number])
        });
    location.reload();
}

async function add_object(object){
    //event.preventDefault();    // prevent page from refreshing
    const root = object.parentElement.parentElement
    const elemId = root.getAttribute("element")
    let response = await fetch("/add", {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json'
           },
            body: JSON.stringify(elemId)
        });
    location.reload();
}
