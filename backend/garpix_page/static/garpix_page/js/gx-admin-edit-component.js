document.addEventListener('DOMContentLoaded', () => {
    const components = Array.from(document.querySelectorAll('[data-gx-component]'));
    if (components.length == 0) {
        return;
    }

    let activeComponent = null;
    let firstComponent = null;
    const editBlock = createEditBlock();

    components.forEach(component => {
        if (component.dataset.gxComponent === "") {
            return;
        }
        if (firstComponent === null) {
            firstComponent = component;
        }

        component.addEventListener('mouseenter', function() {
            if (activeComponent === null || !activeComponent.isSameNode(this)) {
                updateComponent(this);
            }
        });
        component.addEventListener('mouseleave', function(e) {
            const overlappedElements = document.elementsFromPoint(e.clientX, e.clientY);
            for (let i = 0; i < overlappedElements.length; i++) {
                let el = overlappedElements[i];
                if (el.dataset.gxComponent != null
                    && el.dataset.gxComponent !== ""
                    && !activeComponent.isSameNode(el)
                ) {
                    updateComponent(el);
                    break;
                }
            }
        })
    });

    if (firstComponent) {
        updateComponent(firstComponent);
    } else {
        editBlock.remove();
    }

    function createEditBlock() {
        const editBlock = document.createElement('a');
        editBlock.target = '_blank';
        editBlock.classList.add('gx-admin-edit-block');
        editBlock.addEventListener('mouseenter', () => {
            activeComponent.classList.add('gx-admin-component-highlight');
        });
        editBlock.addEventListener('mouseleave', () => {
            activeComponent.classList.remove('gx-admin-component-highlight');
        });
        document.body.insertAdjacentElement('beforeend', editBlock);

        return editBlock;
    }

    function getComponentOffset(component) {
        const rect = component.getBoundingClientRect();
        return {
            left: rect.left + window.scrollX,
            top: rect.top + window.scrollY
        };
    }

    function updateComponent(component) {
        activeComponent = component;
        const offset = getComponentOffset(component);
        editBlock.href = component.dataset.gxComponent;
        editBlock.style.top = `${offset.top}px`;
        editBlock.style.left = `${offset.left}px`;
    }
});
