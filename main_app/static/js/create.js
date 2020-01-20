function add_option() {
    let adder = document.getElementById('adder');
    adder.parentNode.removeChild(adder);

    let counter = document.getElementById('count');
    counter.value = Number(counter.value) + 1;

    let p = document.createElement('div');
    p.className = 'row card-text mt-2';

    inp = document.createElement('input');
    inp.type = 'text';
    inp.name = 'option' + counter.value;
    inp.placeholder = "Введите свой вариант ответа";
    p.appendChild(inp);

    add = document.createElement('button');
    add.type = 'button';
    add.id = 'adder';
    add.className = "btn btn-outline-success ml-2 btn-sm px-2";
    add.onclick = function() { add_option() };
    add.textContent = "+";
    p.appendChild(add);

    let cont = document.getElementById("options_container");
    cont.appendChild(p);
}

function delete_option(id) {
    o = document.getElementById(id)
    btn = document.getElementById("del_"+id)
    o.parentNode.removeChild(o)
    btn.parentNode.removeChild(btn)
}