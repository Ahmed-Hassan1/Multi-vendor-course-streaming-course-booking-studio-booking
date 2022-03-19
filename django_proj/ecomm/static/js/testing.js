document.addEventListener('DOMContentLoaded',()=>{
    document.getElementById('inst').addEventListener('input',handleSecetion);
});

var defaultOption = document.getElementById("inst");
console.log(defaultOption.value)

for(var i=0; i<defaultOption.length;i++)
{
    let x=document.getElementById(defaultOption[i].value);
    if(defaultOption[i].value==defaultOption.value)
    {
        x.style.display="block"
    }
    else
    {
        x.style.display="none"
    }
}

function handleSecetion(ev)
{
    let select = ev.target;
    var optionMenu=document.getElementById("inst");
    for(var i=0; i<optionMenu.length;i++)
    {
        let x=document.getElementById(optionMenu[i].value);
        if(optionMenu[i].value==select.value)
        {
            x.style.display="block"
        }
        else
        {
            x.style.display="none"
        }
    }
    
    
}

document.addEventListener("change",submitform)

function submitform()
{
      document.myform.submit();
}