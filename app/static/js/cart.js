function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        console.info(data)
        let items = document.getElementsByClassName('cart-counter');
        for (let item of items)
            item.innerText = data.total_quantity
    })
}

function updateCart(id, obj) {
    obj.disabled = true;
    fetch(`/api/cart/${id}`, {
        method: 'put',
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        obj.disabled = false;
        console.info(data)
        let items = document.getElementsByClassName('cart-counter');
        for (let item of items)
            item.innerText = data.total_quantity

        let amount = document.getElementById('cart-amount')
        const VND = new Intl.NumberFormat('en-US', {
            currency: 'USD',
            minimumFractionDigits: 0
        })

        amount.textContent = "Tổng tiền: " + VND.format(data.total_amount) + " VNĐ";
    })
}

function deleteCart(id, obj) {
    if (confirm("Bạn có chắc chắn muốn xóa không?") === true) {
        obj.disabled = true;
        fetch(`/api/cart/${id}`, {
            method: 'delete'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            obj.disabled = false;
            console.info(data)
            let items = document.getElementsByClassName('cart-counter');
            for (let item of items)
                item.innerText = data.total_quantity

            let d = document.getElementById(`product${id}`)
            d.style.display = "none";

            let amount = document.getElementById('cart-amount')
            const VND = new Intl.NumberFormat('en-US', {
                currency: 'USD',
                minimumFractionDigits: 0
            })

            amount.textContent = "Tổng tiền: " + VND.format(data.total_amount) + " VNĐ";
        })
    }
}

function pay() {
    if (confirm('Bạn có chắc chắn muốn thanh toán') === true) {
        fetch('/api/pay' , {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload()
            else
                alert(data.err_msg)
        })
    }
}