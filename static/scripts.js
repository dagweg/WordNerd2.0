const ind = parseInt(getCookie('iob'))  // getting index of button cookie
var won = false, first_load = false     
var correctWord = ''                    // stores the correct word
const incorrectWord = []                // used for bulbWork - when bulb is clicked

var usedBulb = false                    // if bulb is used at least once
var outBulb = false                     // if ran out of bulb

var diff = ''                           // to keep track of the difficulty

var totalScore = 0;                     // to keep track of total score 

/* Number of times bulb can be clicked */
var bulbChance =
{
    'easy': Math.floor((correctWord.length)/2), 'medium': Math.floor((correctWord.length)/2), 'hard':Math.floor((correctWord.length)/2), 'insane':Math.floor((correctWord.length)/2)
} 

var bulbCount = 
{
    'easy':0, 'medium':0, 'hard':0, 'insane':0
}
var rankScaling =
{
    'barbarian' : 200, 'recruit' : 5000, 'graduate' : 25000, 'researcher': 50000, 'professor':100000
}

var currentRank = ''

function setTotalScore()
{
    req = $.ajax({
        type: 'POST',
        url: '/score',
    });
    
    req.done(function(data)
    {
        window.totalScore = parseInt(data.score_value)
    })
}

function _init_progressbar()
{
    var progressbar = document.getElementById("progress")

    setTimeout(()=>
    {
        if(window.totalScore >= rankScaling['professor'])
        {
            progressbar.style.width = '100%'
            return
        }
        else
        {
            setTimeout(()=>
            {
                progressbar.style.width = Math.floor((window.totalScore*100)/rankScaling[currentRank.toString().toLowerCase()]).toString() + '%'
            }, 100)
        }
    }, 100)

    
    
}

function _init_rank()
{
    setTimeout(()=>
    {
        if(totalScore <= 200)
        {
            window.currentRank = 'barbarian'
        }
        else if(totalScore > 200 && totalScore <= 5000)
        {
            window.currentRank = 'recruit'
        }
        else if(totalScore > 5000 && totalScore < 25000)
        {
            window.currentRank = 'graduate'
        }
        else if(totalScore > 25000 && totalScore <= 50000)
        {
            window.currentRank = 'researcher'
        }
        else
        {
            window.currentRank = 'professor'
        }        
    }, 50)
}

function welcomeClicked()
{
    const overlay = document.querySelector('.overlay')
    const popup = document.querySelector('.popup-div')
    
    overlay.removeAttribute('hidden')
    popup.removeAttribute('hidden')
    overlay.style.scale = 1
    popup.style.scale = 1
    
}

function embarkClicked()
{
    const overlay = document.querySelector('.overlay')
    const popup = document.querySelector('.popup-div')
    
    overlay.style.scale = 0
    popup.style.scale = 0
}

// When the Site Loads.. EXCEPT login, signup, error, validate and verify
function onLoad(correct_word, firstLoad, difficulty)  
{
    setTotalScore()
    _init_progressbar()
    _init_rank()
    setRankText()    

    diff = difficulty.toLowerCase() // keeping track of difficulty

    bulbChance =
    {
        'easy': Math.floor((correct_word.length)/2), 'medium': Math.floor((correct_word.length)/2), 'hard':Math.floor((correct_word.length)/2), 'insane':Math.floor((correct_word.length)/2)
    } 

    // setting both to false on load
    usedBulb = false 
    outBulb = false


    const buttons = document.querySelectorAll('.button-1')
    const diffinfo = document.querySelector('#difficultyInfo')
    var lettercards = document.querySelectorAll('#iletters')
   
    const colors = ['#0c5b80', '#0c7280', '#0c8067'] // colors to choose from
    var randomColor = colors[Math.floor(Math.random() * colors.length)]

    " Selects random color everytime site is loaded "
    for(let i = 0; i < lettercards.length; i++)
    {
        lettercards[i].style.backgroundColor = randomColor;
    }

    buttons[ind].classList.add('button-1-selected')
    firstLoad = firstLoad == 'True' ?  1 : 0
    first_load = Boolean(firstLoad)
    
    if(firstLoad)
    {
        diffinfo.setAttribute('hidden','true')
    }
    else
    {
        diffinfo.removeAttribute('hidden')
    }

    dragWork(correct_word)
    correctWord = correct_word


}


// When Login Page Loads
function onLoadLogin(msg)
{
    const successRegDiv = document.querySelector('#isuccess-reg-div')
    successRegDiv.setAttribute('hidden', 'true')
    if(msg.length > 0)
    {
        successRegDiv.removeAttribute('hidden')
    }
}

var pressedCount = 0
function deleteClicked()
{
    
    if(pressedCount < 5)
    {
        req = $.ajax(
        {
            method: 'POST',
            url: '/raze',
            data: {'flag':1}
        })
    }
    else
    {
        window.location.reload()
    }
    window.pressedCount++
        
    
}


var infoTold = false
function deleteInfo()
{
    if(!window.infoTold)
        alert('Click 6 times to delete your account.')
    window.infoTold = true

}




// If bulb button is clicked
function bulbWork(correct_word)
{
    const ranout = document.querySelector('#outofbulb')
    
    usedBulb = true

    switch(diff)
    {
        case 'easy':
            // Bulb ran out
            if(window.bulbCount['easy'] >= window.bulbChance['easy'])
            {
                outBulb = true

                ranout.removeAttribute('hidden')
                setTimeout(()=>
                {
                    ranout.setAttribute('hidden', 'true')
                },3000)

                return
            } 
            else
            {
                window.bulbCount['easy']++
                break
            }
        case 'medium':
            // Bulb ran out
            if(window.bulbCount['medium'] >= window.bulbChance['medium'])
            {
                outBulb = true
                
                ranout.removeAttribute('hidden')
                setTimeout(()=>
                {
                    ranout.setAttribute('hidden', 'true')
                },3000)
                return
            } 
            else
            {
                window.bulbCount['medium']++
                break
            }
        case 'hard':
            // Bulb ran out
            if(window.bulbCount['hard'] >= window.bulbChance['hard'])
            {
                outBulb = true

                ranout.removeAttribute('hidden')
                setTimeout(()=>
                {
                    ranout.setAttribute('hidden', 'true')
                },3000)
                return
            } 
            else
            {
                window.bulbCount['hard']++
                break
            }
        case 'insane':
            // Bulb ran out
            if(window.bulbCount['insane'] >= window.bulbChance['insane'])
            {
                outBulb = true 

                ranout.removeAttribute('hidden')
                setTimeout(()=>
                {
                    ranout.setAttribute('hidden', 'true')
                },3000)
                return
            }
            else
            {
                window.bulbCount['insane']++
                break
            }
        default:
            return
    }

    const letters = document.querySelectorAll('.lettercard')
    const correctWord = [...correct_word]
 

    ' Pushing the currect letter combination into incorrectWord for later comparison with correctWord'
    for(const letter of letters)
        incorrectWord.push((letter.outerText).toUpperCase())


    // popping the last elements if iw > cw 
    if(incorrectWord.length > correctWord.length)
        for(let k = 0; k < correctWord.length; k++)
            incorrectWord.pop()
    
    // An algorithm to match the correct word using swapping
    for(let i = 0; i < correctWord.length; i++)
    {
        
        if(incorrectWord[i] !== correctWord[i].toUpperCase())
        {
           
            var tmp = incorrectWord[i]
            
            incorrectWord[i] = correctWord[i].toUpperCase()

            for(let j = i+1; j < correctWord.length; j++)
            {
                
                if(incorrectWord[j] === correctWord[i].toUpperCase())
                {
                    incorrectWord[j] = tmp
                    break
                }
            }
            letters[i].style.backgroundColor = '#309103'  // changing color of corrected letter to green
            
            break
        }   
    }

    let i = 0

    letters.forEach(letter => 
    {
        letter.innerHTML = incorrectWord[i++]
        
    })

}

// COOKIE FUNCS
function setCookie(cname, cvalue, exdays) 
{
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) 
{
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

// Applies color to a button using cookies \_()_/
function changeColor(i)
{   
    const diffs = [...document.querySelectorAll('.button-1')]
    setCookie('iob', i) // iob means indexofbutton 

    for(let j = 0; j < 4; j++)
    {
        diffs[j].classList.remove('button-1-selected')
    }
    diffs[i].classList.add('button-1-selected')
}

// helper function to check if two arrays are equal
function checkArrays(arr1, arr2)
{
    if(arr1.length != arr2.length)
    {
        return false
    }
    for(let i = 0; i < arr2.length; i++)
    {   
        if(arr1[i] != arr2[i])
        {
            return false
        }
    }
    return true
    
}

// If letters are being dragged then don't check answer
const g_letters = document.querySelectorAll('.lettercard')
g_letters.forEach(g_letter => {
    if(!g_letter.classList.contains('.dragging'))
    {
        setInterval(()=>
        {
            setRank()
            setProgressBar()
            validateLetterCombo(correctWord)
        }, 500) // checking if correct word if found every 0.5 second
    }
})

function setRankText() 
{ 
    var rank = document.getElementById('rank')
    
    setTimeout(()=>{ 
        rank.innerHTML = 'Rank: ' + window.currentRank.charAt(0).toUpperCase() + window.currentRank.slice(1)
    }, 150)
    
}

// Checks if the words are the same
function validateLetterCombo(correct_word)
{
    var lettersAll = document.querySelectorAll('.letters')   
    
    var m_word = []
    
    var word = [...correct_word.toLowerCase()] // converting correct_word to iterable array
    
    lettersAll.forEach(letter=>
    {
        m_word.push((letter.outerText).toLowerCase())
    })
    
    // If you win
    if(checkArrays(word, m_word)) 
    {
        won = true // a flag that tells the game is won

        setScoreScale() 
        setScoreNotification()

        // this will tell python that the answer was correct and python will save the word into the database so that it won't be displayed again
        server.isCorrect() 
        setScoreLabel()
        setProgressBar()
        
        const containerdiv = document.querySelector('#letter-img-div')
        var compliment = document.querySelector('#icompliment')

        const image = document.createElement('img')

        var children = containerdiv.children

        containerdiv.classList.remove('container')

        // removing draggable feature from letters after game is won
        for(let i=0; i < children.length; i++)
        {
            children[i].classList.remove('letters')
            children[i].classList.remove('draggable')
            children[i].removeAttribute('draggable')
            children[i].removeAttribute('ondragstart')
            children[i].removeAttribute('ondragend')
            
        }



        // Turning the cards green after won
        var lettercards = document.querySelectorAll('#iletters')
        
        lettercards.forEach(letter=>{
            if(!letter.classList.contains('.dragging'))
            {
                setTimeout(()=>{
                for(let i = 0; i < lettercards.length; i++)
                    lettercards[i].style.backgroundColor = '#309103';
                }, 250)
        
                // Showing check-mark after some delay
                setTimeout(()=>{
                    image.id = 'check-mark'
                    image.classList.add("letter-img-child")
                    image.style.marginTop = ''
                    image.hidden = false
                    image.src = '/static/Content/--check.png'
                    image.alt = 'Correct'
                    containerdiv.append(image)
                }, 275)
                
                // Showing compliment after another delay
                setTimeout(()=>{
                    compliment.removeAttribute('hidden')
                }, 400)
            }
        })

        return true
    }
    
    return false
     
}

// Score scaling + side-effect : returns the score amount
function setScoreScale()
{
    if(usedBulb && outBulb) // You used your bulb and your bulb ran out
    {
        if(diff == 'easy')
        {
            server.scoreScale(bulbChance['easy'])
            return bulbChance['easy']
        }    
        else if(diff == 'medium')
        {
            server.scoreScale(bulbChance['medium'])
            return bulbChance['medium']
        }    
        else if(diff = 'hard')
        {
            server.scoreScale(bulbChance['hard'])
            return bulbChance['hard']
        }    
        else if(diff == 'insane')
        {
            server.scoreScale(bulbChance['insane'])
            return bulbChance['insane']
        }    

    }
    else if(usedBulb && !outBulb) // You used your bulb but it didn' run out
    { 
        if(diff == 'easy')
        {
            server.scoreScale(2 * bulbChance['easy'])
            return 2 * bulbChance['easy']
        }    
        else if(diff == 'medium')
        {
            server.scoreScale(2 * bulbChance['medium'])
            return 2 * bulbChance['medium']
        }    
        else if(diff = 'hard')
        {
            server.scoreScale(2 * bulbChance['hard'])
            return 2 * bulbChance['hard']
        }    
        else if(diff == 'insane')
        {
            server.scoreScale(2 * bulbChance['insane'])
            return 2 * bulbChance['insane']
        }    
    }
    else                           // if you didn't use any bulb token
    {
        if(diff == 'easy')
        {
            server.scoreScale(3 * bulbChance['easy'])
            return 3 * bulbChance['easy'] 
        }    
        else if(diff == 'medium')
        {
            server.scoreScale(3 * bulbChance['medium'])
            return 3 * bulbChance['medium']
        }    
        else if(diff = 'hard')
        {
            server.scoreScale(3 * bulbChance['hard'])
            return 3 * bulbChance['hard']
        }    
        else if(diff == 'insane')
        {
            server.scoreScale(3 * bulbChance['insane'])
            return 3 * bulbChance['insane']
        }    
    }
}

function setScoreNotification()
{

    const scoreN = document.querySelector('#scorenotifier')
    const scoreL = document.querySelector('#scorenotifierlabel')
    scoreL.innerHTML = '+' + setScoreScale()
    scoreN.removeAttribute('hidden')
}

function setScoreLabel()
{
    setTimeout(() => {
        req = $.ajax({
            type: "POST",
            url: "/score",
        });
        
        req.done(function(data)
        {
            setTimeout(() => {
                document.querySelector('#scoreLabel').innerHTML = data.score_value;
                window.totalScore = data.score_value;
              }, 1000);
        })  
    }, 128);
}

function setProgressBar()
{
    let progressbar = document.getElementById('progress')

    if(window.totalScore >= rankScaling['professor'])
    {
        progressbar.style.width = '100%'
    }
    else
    {
        setTimeout(()=>
        {
            progressbar.style.width = Math.floor((window.totalScore*100)/rankScaling[currentRank]).toString() + '%'
        }, 150)
    }
    
    
    
}

// if GET Hint gets clicked
function hintClick(hint)
{
    let hintDiv = document.getElementById('hintTextDiv');
    let hintArea = document.getElementById('hintTextArea');  

    if(hintDiv.className == 'text-area-1') 
    {
        // hide 
        hintDiv.className = '';
    }
    else
    {
        // show text area
        hintDiv.className = 'text-area-1'
    }

    if(hintArea.innerHTML == '')
    {
        hintArea.innerHTML = hint;
    }
    else
    {
        hintArea.innerHTML = '';
    }
}


function dragWork()
{
    
    const draggables = document.querySelectorAll('.draggable') // it is iterable bc 'All'
    const containers = document.querySelectorAll('.container')
   
    draggables.forEach(draggable => {

        draggable.addEventListener('dragstart', ()=>
        {
            if(won || first_load)
            {
                draggable.classList.remove('dragging')
            }
            else
            {
                draggable.classList.add('dragging')
            }
        })

        draggable.addEventListener('dragend', ()=>{
            draggable.classList.remove('dragging')
        })

    })
    containers.forEach(container => {
        // e - eventlistener
        container.addEventListener('dragover', (e)=>{ 
            e.preventDefault() // disables the default 'drag-disabled' cursor
 
            const afterElement = getDragAfterElement(container, e.clientX)
            const draggable = document.querySelector('.dragging')

            if (afterElement == null)
            {
                container.appendChild(draggable) // if the dragged element isnt above anything append to the last
            }
            else
            {
                container.insertBefore(draggable, afterElement) // if the dragged element is ahead the afterElement then insert before that element
            }

            return
        })
    })
    
    function getDragAfterElement(container, x)
    {
        const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')] // returns the items which don't have the .dragging class but have .draggable class

        return draggableElements.reduce((closest, child)=>{
            const box = child.getBoundingClientRect() // bounding box        
            const offset = x - box.left - box.width/2 // distance between the mouse and the middle of the current child
            if (offset < 0 && offset > closest.offset)
            { 
                return {offset:offset, element:child} // if the distance is 0 or really close to zero it returns the child  
            }
            else
            {
                return closest
            }
        }, {offset: Number.NEGATIVE_INFINITY}).element // .element - to return only the element and not the offset

    }

}