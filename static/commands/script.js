function clearContents(element) {
  element.value = '';
}

async function arrived(object){
    //event.preventDefault();    // prevent page from refreshing
    const root = object.parentElement.parentElement
    const elemId = root.getAttribute("element")
    const image = document.getElementById("")
    let response = await fetch("/arrived", {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json'
           },
            body: JSON.stringify({name:elemId,image:image})
        });
    location.reload();
}

async function create_stock(object){
    const photo = document.getElementById("create_file").files[0];
    const name = document.getElementById("create_text").value;
    const number = document.getElementById("create_number").value;
    if (photo) {
        const reader = new FileReader();

        // Conversion de l'image en Base64
        reader.onload = async function(event) {
            const photoBase64 = event.target.result.split(',')[1]; // Récupère uniquement la partie Base64
            let response = await fetch("/order", {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image: photoBase64,
                    name: name,
                    quantity: number
                })
            });
            location.reload(); // Recharge la page après le succès de l'opération
        };

        reader.readAsDataURL(photo); // Lit le fichier en tant qu'URL de données (Base64)
    } else {
        alert("Veuillez sélectionner une image !");
    }
}
