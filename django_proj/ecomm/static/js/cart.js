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
            addCookieItem(prodID,action);
        }
        else updateUserOrder(prodID,action);
    })
}

function addCookieItem(prodID,action)
{
    console.log('Not loged in..');

    if(action ==  'add')
    {
        if(cart[prodID]== undefined)
        {
            cart[prodID] = {'quantity':1}
        }
    }

    if(action ==  'remove')
    {
        delete cart[prodID];
    }
    console.log(cart)

    document.cookie = 'cart='+ JSON.stringify(cart) + ";domian=;path=/"
    location.reload()
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