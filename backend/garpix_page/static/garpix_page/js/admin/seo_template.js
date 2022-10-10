window.onload = function(){
    let rule_field = document.querySelector('#id_rule_field');
    let model_rule_value = document.querySelector('.field-model_rule_value');
    let rule_value = document.querySelector('.field-rule_value');

    if (rule_field.value === 'model_name') {
        model_rule_value.classList.remove('admin-none');
        rule_value.classList.add('admin-none');
    }
    else {
        model_rule_value.classList.add('admin-none');
        rule_value.classList.remove('admin-none');
    }

    rule_field.addEventListener('change', (event) => {
        if (event.currentTarget.value === 'model_name') {
            model_rule_value.classList.remove('admin-none');
            rule_value.classList.add('admin-none');
        }
        else {
            model_rule_value.classList.add('admin-none');
            rule_value.classList.remove('admin-none');
        }
    });
}