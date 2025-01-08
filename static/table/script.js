function clearContents(element) {
  element.value = '';
}


async function remove_object(object){
    //event.preventDefault();    // prevent page from refreshing
    const root = object.parentElement.parentElement
    const elemId = root.getAttribute("element")
    var number = root.querySelector("#remove").value
    let response = await fetch("/remove", {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json'
           },
            body: JSON.stringify({name:elemId,quantity:number})
        });
    location.reload();
}

async function add_object(object){
    //event.preventDefault();    // prevent page from refreshing
    const root = object.parentElement.parentElement
    const elemId = root.getAttribute("element")
    var number = root.querySelector("#add").value
    let response = await fetch("/add", {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json'
           },
            body: JSON.stringify({name:elemId, quantity: number})
        });
    location.reload();
}

async function create_stock(object){
    const photo = document.getElementById("create_file").files[0];
    const name = document.getElementById("create_text").value;
    const number = document.getElementById("create_number").value;
    console.log(photo,name,number);
}