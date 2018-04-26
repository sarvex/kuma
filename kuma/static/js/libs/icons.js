(function() {
    'use strict';

    /**
     * Creates and returns a new SVG element, setting the values of the appropriate
     * attributes. All parameters are required.
     * @param {String} classNames - The class name or names to set
     * @param {String} width - The width of the SVG element to set
     * @param {String} height - The height of the SVG element to set
     * @param {String} viewBox - The value for the viewBox attribute to set
     * @returns The SVG element
     */
    function getSVGElement(classNames, width, height, viewBox) {
        var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('class', classNames);
        svg.setAttribute('version', '1.1');
        svg.setAttribute('width', width);
        svg.setAttribute('height', height);
        svg.setAttribute('viewBox', viewBox);
        svg.setAttribute('aria-hidden', true);
        return svg;
    }

    /**
     * Creates and returns a empty SVG `path` element
     * @returns A SCG `path` element
     */
    function getPathElement() {
        return document.createElementNS('http://www.w3.org/2000/svg', 'path');
    }

    /**
     * Creates and returns the relevant icon SVG based on the `iconName` parameter
     * @param {String} iconName - The name of the icon to return
     * @returns The icon as an SVG element
     */
    function getIcon(iconName) {
        switch(iconName) {
            case 'pencil':
                var svg = getSVGElement('icon icon-pencil', '24', '28', '0 0 24 28');
                var path = getPathElement();
                path.setAttribute('d', 'M5.672 24l1.422-1.422-3.672-3.672-1.422 1.422v1.672h2v2h1.672zM13.844 9.5c0-0.203-0.141-0.344-0.344-0.344-0.094 0-0.187 0.031-0.266 0.109l-8.469 8.469c-0.078 0.078-0.109 0.172-0.109 0.266 0 0.203 0.141 0.344 0.344 0.344 0.094 0 0.187-0.031 0.266-0.109l8.469-8.469c0.078-0.078 0.109-0.172 0.109-0.266zM13 6.5l6.5 6.5-13 13h-6.5v-6.5zM23.672 8c0 0.531-0.219 1.047-0.578 1.406l-2.594 2.594-6.5-6.5 2.594-2.578c0.359-0.375 0.875-0.594 1.406-0.594s1.047 0.219 1.422 0.594l3.672 3.656c0.359 0.375 0.578 0.891 0.578 1.422z');
                svg.appendChild(path);
                return svg;
            case 'close':
                var svg = getSVGElement('icon icon-close', '24', '28', '0 0 24 28');
                var path = getPathElement();
                path.setAttribute('d', 'M20.281 20.656c0 0.391-0.156 0.781-0.438 1.062l-2.125 2.125c-0.281 0.281-0.672 0.438-1.062 0.438s-0.781-0.156-1.062-0.438l-4.594-4.594-4.594 4.594c-0.281 0.281-0.672 0.438-1.062 0.438s-0.781-0.156-1.062-0.438l-2.125-2.125c-0.281-0.281-0.438-0.672-0.438-1.062s0.156-0.781 0.438-1.062l4.594-4.594-4.594-4.594c-0.281-0.281-0.438-0.672-0.438-1.062s0.156-0.781 0.438-1.062l2.125-2.125c0.281-0.281 0.672-0.438 1.062-0.438s0.781 0.156 1.062 0.438l4.594 4.594 4.594-4.594c0.281-0.281 0.672-0.438 1.062-0.438s0.781 0.156 1.062 0.438l2.125 2.125c0.281 0.281 0.438 0.672 0.438 1.062s-0.156 0.781-0.438 1.062l-4.594 4.594 4.594 4.594c0.281 0.281 0.438 0.672 0.438 1.062z');
                svg.appendChild(path);
                return svg;
            case 'undo':
                var svg = getSVGElement('icon icon-undo', '24', '28', '0 0 24 28');
                var path = getPathElement();
                path.setAttribute('d', 'M24 14c0 6.609-5.391 12-12 12-3.578 0-6.953-1.578-9.234-4.328-0.156-0.203-0.141-0.5 0.031-0.672l2.141-2.156c0.109-0.094 0.25-0.141 0.391-0.141 0.141 0.016 0.281 0.078 0.359 0.187 1.531 1.984 3.828 3.109 6.312 3.109 4.406 0 8-3.594 8-8s-3.594-8-8-8c-2.047 0-3.984 0.781-5.437 2.141l2.141 2.156c0.297 0.281 0.375 0.719 0.219 1.078-0.156 0.375-0.516 0.625-0.922 0.625h-7c-0.547 0-1-0.453-1-1v-7c0-0.406 0.25-0.766 0.625-0.922 0.359-0.156 0.797-0.078 1.078 0.219l2.031 2.016c2.203-2.078 5.187-3.313 8.266-3.313 6.609 0 12 5.391 12 12z');
                svg.appendChild(path);
                return svg;
            case 'play':
                var svg = getSVGElement('icon icon-play', '24', '28', '0 0 24 28');
                var path = getPathElement();
                path.setAttribute('d', 'M12 2c6.625 0 12 5.375 12 12s-5.375 12-12 12-12-5.375-12-12 5.375-12 12-12zM18 14.859c0.313-0.172 0.5-0.5 0.5-0.859s-0.187-0.688-0.5-0.859l-8.5-5c-0.297-0.187-0.688-0.187-1-0.016-0.313 0.187-0.5 0.516-0.5 0.875v10c0 0.359 0.187 0.688 0.5 0.875 0.156 0.078 0.328 0.125 0.5 0.125s0.344-0.047 0.5-0.141z');
                svg.appendChild(path);
                return svg;
            case 'book':
                var svg = getSVGElement('icon icon-book', '24', '28', '0 0 24 28');
                var path = getPathElement();
                path.setAttribute('d', 'M25.609 7.469c0.391 0.562 0.5 1.297 0.281 2.016l-4.297 14.156c-0.391 1.328-1.766 2.359-3.109 2.359h-14.422c-1.594 0-3.297-1.266-3.875-2.891-0.25-0.703-0.25-1.391-0.031-1.984 0.031-0.313 0.094-0.625 0.109-1 0.016-0.25-0.125-0.453-0.094-0.641 0.063-0.375 0.391-0.641 0.641-1.062 0.469-0.781 1-2.047 1.172-2.859 0.078-0.297-0.078-0.641 0-0.906 0.078-0.297 0.375-0.516 0.531-0.797 0.422-0.719 0.969-2.109 1.047-2.844 0.031-0.328-0.125-0.688-0.031-0.938 0.109-0.359 0.453-0.516 0.688-0.828 0.375-0.516 1-2 1.094-2.828 0.031-0.266-0.125-0.531-0.078-0.812 0.063-0.297 0.438-0.609 0.688-0.969 0.656-0.969 0.781-3.109 2.766-2.547l-0.016 0.047c0.266-0.063 0.531-0.141 0.797-0.141h11.891c0.734 0 1.391 0.328 1.781 0.875 0.406 0.562 0.5 1.297 0.281 2.031l-4.281 14.156c-0.734 2.406-1.141 2.938-3.125 2.938h-13.578c-0.203 0-0.453 0.047-0.594 0.234-0.125 0.187-0.141 0.328-0.016 0.672 0.313 0.906 1.391 1.094 2.25 1.094h14.422c0.578 0 1.25-0.328 1.422-0.891l4.688-15.422c0.094-0.297 0.094-0.609 0.078-0.891 0.359 0.141 0.688 0.359 0.922 0.672zM8.984 7.5c-0.094 0.281 0.063 0.5 0.344 0.5h9.5c0.266 0 0.562-0.219 0.656-0.5l0.328-1c0.094-0.281-0.063-0.5-0.344-0.5h-9.5c-0.266 0-0.562 0.219-0.656 0.5zM7.688 11.5c-0.094 0.281 0.063 0.5 0.344 0.5h9.5c0.266 0 0.562-0.219 0.656-0.5l0.328-1c0.094-0.281-0.063-0.5-0.344-0.5h-9.5c-0.266 0-0.562 0.219-0.656 0.5z');
                svg.appendChild(path);
                return svg;
            default: {
                return;
            }
        }
    }

    // expose the `getIcon` function to the global scope
    window.mdnIcons = {
        getIcon: function(iconName) {
            return getIcon(iconName);
        }
    }

})();
