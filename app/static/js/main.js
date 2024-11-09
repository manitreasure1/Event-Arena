function toggleReadMe(ReadMoreElement){
    const targetId = ReadMoreElement.getAttribute('data-target')
    const moreInfo = document.getElementById(targetId);

    if(moreInfo.style.display === 'none' || moreInfo.style.display === ''){
        moreInfo.style.display = 'block';        
    }else{
        moreInfo.style.display = 'none'
    } 
}

function vistEvent(){
    const displayForm = document.getElementById('registerForm');
    displayForm.style.display = displayForm.style.display === 'none'? 'block' :'block';
}
function toggleForm() {
    const displayForm = document.getElementById('registerForm');
    displayForm.style.display = displayForm.style.display === 'block' ? 'none' : 'none';
}

function showTnC() {
    const tncContent = document.getElementById('tncContent');
    tncContent.style.display = tncContent.style.display === 'block' ? 'none' : 'block';
}

function moreAboutEvent(ShowMoreAboutEvent){
    const moreAbout_event = ShowMoreAboutEvent.getAttribute('data-target')
    const sessionEvent = document.getElementById(moreAbout_event);          
    sessionEvent.style.display = sessionEvent.style.display ==='none' ? 'block': 'none'
}



