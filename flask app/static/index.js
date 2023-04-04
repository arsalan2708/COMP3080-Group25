function init() {

    main = document.getElementById('main')
    main.addEventListener('change', () => {
        removeSubSelects('all')
        emptyMainBody()


        if (main.value != 'people') {
            const secondSel = createSelection(main.value, 'second', ['all', 'byTitle', 'yearReleased', 'genre', 'rating'])

            if (main.value == 'tvSeries') secondSel.innerHTML += '<option value="hasEnded">is Completed</option>'
            else if (main.value == 'movies') secondSel.innerHTML += '<option value="runTime">by Run-Time</option>'

            document.querySelector('.qSelects').append(secondSel)
            secondOnChange(secondSel)

        } else {
            const secondSel = createSelection(main.value, 'second', ['all', 'byName', 'birthYear', 'isAlive', 'byProfession'])
            document.querySelector('.qSelects').append(secondSel)
            secondOnChange(secondSel)
        }
    })


}


function createSelection(fr, id, selectVal) {
    const sel = document.createElement('select')
    sel.setAttribute('id', id)
    sel.setAttribute('class', 'subSelection')
    sel.selectionFor = fr;

    sel.innerHTML = '<option value="" selected disabled hidden>---Select By---</option>'
    for (opt of selectVal) {
        sel.innerHTML += `<option value='${opt}'> ${opt} </option>`
    }

    return sel
}


function secondOnChange(second) {
    const main = document.querySelector('#main')

    second.addEventListener('change', () => {
        removeSubSelects('last')
        if (second.value == 'genre') {
            load('getAllGenre').then((r) => {
                const sel = createSelection(second.value, 'third', r)
                document.querySelector('.qSelects').append(sel)

            })

        } else if (['byName', 'byTitle'].includes(second.value)) {
            document.querySelector('.qSelects').append(createSelection(second.value, 'third', ['ascending', 'descending', 'startingWith']))

        } else if (second.value == 'all') {
            processAllRequest(main.value)
        }

    });

}

function processAllRequest(mValue) {
    const qry = {
        titles: "titles where fType in ('movie','tvSeries')",
        movies: "titles where fType in ('movie')",
        tvSeries: "titles where fType in ('tvSeries')",
        people: "people"
    };

    load(`/getAll/${qry[mValue]}`).then((res) => {
        createTable(res)
    })
}

function removeSubSelects(amount) {
    const child = document.querySelectorAll('.subSelection')
    if (child != null && amount == 'all') {
        for (c of child) {
            c.parentNode.removeChild(c)
        }
    } else if (child.length > 1 && amount == 'last') {
        child[child.length - 1].parentNode.removeChild(child[child.length - 1])
    }
}

function emptyMainBody() {
    const currDiv = document.querySelector('.content')
    const emptyDiv = document.createElement('div')
    emptyDiv.setAttribute('class', 'content')

    currDiv.replaceWith(emptyDiv)
}


function createTable(info) {
    emptyMainBody()
    const currDiv = document.querySelector('.content')
    const table = document.createElement('table')
    table.setAttribute('class', 'qTable')

    const tableHead = document.createElement('thead')
    const tableBody = document.createElement('tbody')

    const header = info.shift()
    header.unshift('rowNum')
    var row = document.createElement('tr')
    for (val of header) row.innerHTML += `<th>${val}</th>`
    tableHead.append(row)

    let count = 0;
    info.forEach(element => {
        element.unshift(count+1)
        count +=1
    });

    const slider = document.createElement('input')
    slider.setAttribute('type', 'range')
    slider.setAttribute('id', 'slider')
    let min = 5 > info.length ? info.length : 5
    let max = info.length
    let currValue = Math.floor((max + min) / 3)
    slider.max = max+1;
    slider.min = min-1;
    slider.value = currValue


    count = 0
    for (r of info) {
        row = document.createElement('tr')
        for (c of r) row.innerHTML += `<td>${c}</td>`
        tableBody.append(row)
        count++;
        if (count > slider.value) break;
    }

    slider.addEventListener('change', (e) => {
        console.log(slider.value)
        const tableBody = document.querySelector('tbody')
        const newtBody = document.createElement('tbody')
        let count = 0
        for (r of info) {
            row = document.createElement('tr')
            for (c of r) row.innerHTML += `<td>${c}</td>`
            newtBody.append(row)
            count++;
            if (count >= slider.value) break;
        }

        tableBody.replaceWith(newtBody)
    })

    table.append(tableHead, tableBody)
    currDiv.append(slider, table)
}














window.addEventListener('load', init)




// create custom Alph button:
function createAlph() {
    const d = document.createElement('span')
    d.setAttribute('class', 'subSelection')
    d.innerHTML = `<p id="alph">A</p>
                    <span class="btnGroup">
                        <button>+</button>
                        <button>-</button>
                    </span>`

    logicAlph(d)
    return d;
}



function logicAlph(d) {
    const alph = d.querySelector('#alph')
    const btn = d.querySelector('.btnGroup').children

    btn[0].addEventListener('click', () => {
        const chrCode = alph.innerText.charCodeAt(0);
        if (chrCode < 90) {
            alph.innerText = String.fromCharCode(chrCode + 1);
        }

    })

    btn[1].addEventListener('click', () => {
        const chrCode = alph.innerText.charCodeAt(0);
        if (chrCode > 65) {
            alph.innerText = String.fromCharCode(chrCode - 1);
        }
    })

}



//send the post request to flask app
function load(url) {
    return new Promise(async function (resolve, reject) {
        // do async thing
        const res = await fetch(url, { method: "POST" })
        // resolve
        resolve(res.json())

        reject(new Error('Error No results found'))
    })
}


