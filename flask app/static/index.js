function init(){

    main = document.getElementById('main')
    main.addEventListener('change',()=>{
        if(main.value != 'people'){

        }
    })

    console.log(main)

}


function createSelection(){
    
}


function load(url,prm) {
    return new Promise(async function (resolve, reject) {
        // do async thing
        const res = await fetch(url, { method: "POST" })
        // resolve
        resolve(res.json())
    })
}

window.addEventListener('load',init)


