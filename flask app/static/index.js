function init(){

    main = document.getElementById('main')
    main.addEventListener('change',()=>{
        
        removeSubSelects('second')
        removeSubSelects ('third')
       
        if(main.value != 'people'){
            const secondSel = createSelection(main.value,'second', ['all','yearReleased','genre','rating'])
            if (main.value == 'tvSeries')
                secondSel.innerHTML += '<option value="hasEnded">is Completed</option>'
            else if (main.value == 'movies'){
                secondSel.innerHTML += '<option value="runTime">by Run-Time</option>'
            }
            document.querySelector('body').append(secondSel)
            secondOnChange(secondSel)
        }else{
            const secondSel = createSelection(main.value,'second', ['all','birthYear','isAlive','byAlphabet','byProfession'])
            document.querySelector('body').append(secondSel)
            secondOnChange(secondSel)
        }
    })

 
}


function createSelection(fr,id,selectVal){
    const sel = document.createElement('select')
    sel.setAttribute('id',id)
    sel.selectionFor = fr;

    sel.innerHTML = '<option value="" selected disabled>---Select By---</option>'
        for (opt of selectVal){
            sel.innerHTML += `<option id='${opt}'> ${opt} </option>`}
    
    return sel 
}

function secondOnChange(second){
    const main = document.querySelector('#main')
    
    second.addEventListener('change',()=>{
        if (second.value == 'genre'){
            load('getAllGenre').then((r)=>{
                const sel = createSelection(second.value, 'third', r)
                document.querySelector('body').append(sel)

            } )
    }
});
    
}




function removeSubSelects (id){
    const hasChild = document.querySelector('body').querySelector(`#${id}`) != null
        if (hasChild){
            document.querySelector('body').removeChild(document.querySelector(`#${id}`))
        }
}



function load(url) {
    return new Promise(async function (resolve, reject) {
        // do async thing
        const res = await fetch(url, { method: "POST" })
        // resolve
        resolve(res.json())
    })
}

window.addEventListener('load',init)


