function init(){

    main = document.getElementById('main')
    main.addEventListener('change',()=>{
        const hasSecond = document.querySelector('body').querySelector('#second') != null
        if (hasSecond){
            document.querySelector('body').removeChild(document.querySelector('#second'))
        }
       
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
            const secondSel = createSelection(main.value,'second', ['birthYear','isAlive','byAlphabet'])
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
            console.log(opt)
        sel.innerHTML += `<option id='${opt}'> ${opt} </option>`
    }
    
    return sel 
}

function secondOnChange(second){
    const main = document.querySelector('#main')



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


