function init() {

    main = document.getElementById('main')
    main.addEventListener('change', () => {
        removeSubSelects('all')
        emptyMainBody()


        if (main.value != 'people') {
            const secondSel = createSelection(main.value, ['all', 'byTitle', 'yearReleased', 'genre'])

            if (main.value == 'tvSeries') secondSel.innerHTML += '<option value="completed">Completed</option> <option value="onGoing">on Going</option> <option value="rating">By Rating</option>'
            else if (main.value == 'movie') secondSel.innerHTML += '<option value="runTime">by Run-Time</option> <option value="rating">By Rating</option>'

            document.querySelector('.qSelects').append(secondSel)
            secondOnChange(secondSel)

        } else {
            const secondSel = createSelection(main.value, ['all', 'byName', 'birthYear', 'isAlive', 'hasPassedAway','byProfession'])
            document.querySelector('.qSelects').append(secondSel)
            secondOnChange(secondSel)
        }
    })


}


function createSelection(id, selectVal) {
    const sel = document.createElement('select')
    sel.setAttribute('id', id)
    sel.setAttribute('class', 'subSelection')

    sel.innerHTML = '<option value="" selected disabled hidden>---Select By---</option>'
    for (opt of selectVal) {
        sel.innerHTML += `<option value='${opt}'> ${opt} </option>`
    }

    return sel
}


function secondOnChange(second) {
    const main = document.querySelector('#main')

    second.addEventListener('change', () => {
        removeSubSelects('last',second)
        if (second.value == 'genre') {
            load('getAllGenre').then((r) => {
                processGorP(main.value,second.value,r)
            })
        }if (second.value == 'byProfession') {
            load('getProfessions').then((r) => {
                processGorP(main.value,second.value,r)
            })

        } else if (['byName', 'byTitle'].includes(second.value)) {
            processbyTitleORbyName(main.value,second.value, createSelection(second.value, ['ascending', 'descending', 'startingWith']))

        } else if (second.value == 'all') {
            processAllRequest(main.value)
        } else if(['isAlive','hasPassedAway'].includes(second.value)){
            const wht = second.value=='isAlive' ? 'null' : 'not null'
            const q = `people where deathYear is ${wht} order by birthYear`
            load(`/getAll/${q}`).then((r)=>{createTable(r)})
        } else if(['completed','onGoing'].includes(second.value)){
            const wht = second.value=='onGoing' ? '=0' : '>0'
            const q = `t.*, tv.endYear from titles t join tvSeries tv on tv.tconst=t.tconst where tv.endYear ${wht}  order by t.startYear`
            load(`/get/${q}`).then((r)=>{createTable(r)})
        } else if(['yearReleased','runTime','rating','birthYear'].includes(second.value)){
            const sel = createSelection(second.value, ['equal', 'before', 'after','inBetween'])
            document.querySelector('.qSelects').append(sel)
        }

    });

}

function processAllRequest(mValue) {
    const qry = {
        titles: "/getAll/titles where fType in ('movie','tvSeries') order by startYear",
        movie:  `get/t.* , m.runTime, r.rating from titles t 
        join movies m on t.tconst = m.tconst  join ratings r on t.tconst = r.tconst order by t.startYear`,
        tvSeries: `get/ titles.*, tv.endYear, round(rating, 2)
        from(titles join  tvSeries tv on tv.tconst = titles.tconst join 
                (select E.parent_tconst, avg(rating) as rating
                from episodes E join ratings R ON R.tconst=E.tconst 
                group by E.parent_tconst
                order by parent_tconst desc) ON parent_tconst = titles.tconst)`,
        people: "/getAll/people order by birthYear"
    };

    load(`${qry[mValue]}`).then((res) => {
        createTable(res)
    })
}

function processGorP(val1,val2, res){
    const sel = createSelection(val2, res)
    document.querySelector('.qSelects').append(sel)

    if(val2 == 'genre'){ //dealing with a movie,tvshow or both
        sel.addEventListener('change',(e)=>{
            const mValue = val1;
            const reqVal =  e.target.value;
            const q = `select tconst from genres where genre= '${reqVal}'`
            const qry = {
            titles: `titles where fType in ('movie','tvSeries') and tconst in (${q}) order by startYear`,
            movie: `titles where fType in ('movie') and tconst in (${q}) order by startYear`,
            tvSeries: `titles where fType in ('tvSeries') and tconst in (${q}) order by startYear`}

            load(`/getAll/${qry[mValue]}`).then((res) => {
                createTable(res)
            })
        })
    }else{ //dealing with people 
        sel.addEventListener('change',(e)=>{
            const reqVal =  e.target.value;
            const q = `people where nconst in (select distinct nconst from profession where profession = '${reqVal}')`
            load(`getAll/${q}`).then((res)=>{
                createTable(res)
            })
        })
    }
}

function processbyTitleORbyName (main,sec,sel){
    document.querySelector('.qSelects').append(sel)
    
    sel.addEventListener('change',(e)=>{
        const selVal = e.target.value;
        
        if(selVal != 'startingWith'){
            const q = selVal == 'ascending' ? 'asc' : 'desc' 
            
            if(main != 'people'){
                const qType = main=='titles' ? "('movie','tvSeries')" : `('${main}')`
                const qry = `titles where fType in ${qType} order by title ${q} `
                load(`/getAll/${qry}`).then((res) => {
                    createTable(res)
                })

            }else{
                load(`getAll/people order by name ${q}`).then((res) => {
                    createTable(res)
                })
            }

        }else{document.querySelector('.qSelects').append(createAlph(main))}
    })
}

function removeSubSelects(amount,curr=null) {
    const child = document.querySelectorAll('.subSelection')
    if (child != null && amount == 'all') {
        for (c of child) {
            c.parentNode.removeChild(c)
        }
    } else if (amount == 'last' && curr!=null) {
        for(let i=child.length-1; i>=0 && child[i]!=curr ; i-- ){
            child[i].parentNode.removeChild(child[i])
        }
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
    
    if (info=='No result found'){
        currDiv.append(document.createTextNode(info[0]+'!'))
    }
    else{
    const table = document.createElement('table')
    table.setAttribute('class', 'qTable')

    const tableHead = document.createElement('thead')
    const tableBody = document.createElement('tbody')

    const header = info.shift()
    header.unshift('#')
    indexList = [...Array(header.length).keys()]
    indexList.splice(1,1)
    var row = document.createElement('tr')
    for (val of indexList) row.innerHTML += `<th>${header[val]}</th>`
    tableHead.append(row)

    let count = 0;
    info.forEach(element => {
        element.unshift(count+1)
        count +=1
    });

    const slider = document.createElement('input')
    slider.setAttribute('type', 'range')
    slider.setAttribute('id', 'slider')
    let min = Math.min(5, info.length)
    let max = info.length
    let currValue = Math.min(10,Math.floor((max + min) / 2))
    slider.max = max;
    slider.min = min;
    slider.value = currValue
    slider.step = 1
    const numShowing = document.createElement('p')
    numShowing.setAttribute('class','showingResult')
    numShowing.innerText = `Showing ${slider.value} Results`
    
    
    count = 0
    for (r of info) {
        row = document.createElement('tr')
        for (c of indexList) row.innerHTML += `<td>${r[c]}</td>`
        putLifeIn(row,r)
        tableBody.append(row)
        count++;
        if (count > slider.value) break;
    }

    slider.addEventListener('change', (e) => {
        const len = indexList
        console.log(slider.value)
        const resultShow = document.querySelector('.showingResult')
        const tableBody = document.querySelector('tbody')
        const newtBody = document.createElement('tbody')
        let count = 0
        for (r of info) {
            row = document.createElement('tr')
            for (c of len) row.innerHTML += `<td>${r[c]}</td>`
            putLifeIn(row,r)
            newtBody.append(row)
            count++;
            if (count > slider.value) break;
        }

        resultShow.innerText = `Showing ${slider.value} Results`
        tableBody.replaceWith(newtBody)
    })

    table.append(tableHead, tableBody)
    currDiv.append(numShowing,slider, table)
}
}



function putLifeIn(row,data){

    row.addEventListener('click',()=>{
        const d = data;
        if(d[1].includes('nm')){
            alert(`clicked: (${d[1]}) -> ${d[2]}`)
        }else
            alert(`clicked: (${d[1]}) -> ${d[3]}`)
    })

}













window.addEventListener('load', init)




// create custom Alph button:
function createAlph(main) {
    const d = document.createElement('div')
    d.setAttribute('class', 'subSelection')
    d.setAttribute('id', 'spanContainer')
    d.innerHTML = `<p id="alph">A</p>
                    <span class="btnGroup">
                        <button>+</button>
                        <button>-</button>
                    </span>
                        <button id='queryGo'> Query! </button>
                    `

    logicAlph(main,d)
    return d;
}



function logicAlph(main,d) {
    const alph = d.querySelector('#alph')
    const btn = d.querySelector('.btnGroup').children
    const qBtn = d.querySelector('#queryGo')

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

    qBtn.addEventListener('click',()=>{
        const val = d.querySelector('#alph')
        const type = main!='people' ? 'titles': 'people';
        
        const nType = main != 'titles' ? `fType in ('${main}')` : `fType in ('movie','tvSeries') `
        const sType = main!='people' ? `${nType} and title` : 'name' ;
        
        const qry = `${type} where ${sType} like '${val.innerText}%'`

        load(`/getAll/${qry}`).then((res) => {
            createTable(res)
        })
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


