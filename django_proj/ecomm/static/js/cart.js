var updateBtns = document.getElementsByClassName('update-cart');


for (i=0; i<updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click', function(){
        var prodID = this.dataset.product;
        var action = this.dataset.action;

        console.log('prodid: ',prodID,' Action: ',action);
        console.log('User: ',user);

        if ( user === 'AnonymousUser')
        {
            console.log('user is not logged in');
        }
        else updateUserOrder(prodID,action);
    })
}

function updateUserOrder(prodID,action)
{
    console.log('user is logged');

    url = '/accounts/update-item/'
    fetch(url, {
        method: 'post',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFTOKEN':csrftoken,
        },
        body:JSON.stringify({
            'prodID': prodID,
            'action': action
        })
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        location.reload()
    });
}