/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.searchPage = publicWidget.Widget.extend({
    selector: '#search_container_wrapper_id__main_content',
    events: {
        'click .o_page_item_dashboard_btn': '_onPageChange',
        'click .dropbtn': '_onDropdownToggle',
        'click .dropdown-content a': '_onDropdownItemSelect',
        'click': '_closeDropdowns',
        'click #search_influencer_id': '_render_search_influencer',
    },
    template:"pe_influencer_discovery.search_controller_template",
    async start(){
        this.influencers = await this._get_influencers_data("/api/influencers",{});
        this.currentPageNumber =  1
        debugger;
        const content = renderToElement(this.template,{
            influencers: this.influencers,
            countries: this.countries,
            pagination_info: Array.from({ length: this.influencers.page_count }, (_, index) => index+1),
            currentPageNumber: this.currentPageNumber
        });
        this.$target.html(content)
    },

    _update_page_info(page){
        this.currentPageNumber = page
    },

    async _get_influencers_data(url,data){
    debugger;
      let influencers = this._fetch(url,data)
      return influencers
    },
    async _get_influencers_data_search(url,data){
      let influencers = this._fetch(url,data)
      return influencers
    },

    async _get_pagination_info(url,data){
        let pagination = await this._fetch(url,data)
        return pagination
    },

    async _fetch(url,data,method='POST'){
          try {
            let fetchBody = {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
            if (method=='POST'){
                fetchBody.body = JSON.stringify(data)
            }
            const response = await fetch(url, fetchBody);
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const responseData = await response.json();
            return responseData

        } catch (error) {
            console.error('Error:', error);
        }

    },

    async _onPageChange(event){
        event.preventDefault()
        debugger;
        let way = event.target.dataset.way
        let pageNumber = +event.target.dataset.pagenumber
        if (way=='previous' && pageNumber != 1){
            pageNumber = pageNumber - 1
        }
        if(way=='next' && pageNumber < this.influencers.page_count ){
             pageNumber = pageNumber + 1
        }

        let url = `/api/influencers/${pageNumber}`
        let next_page_items = await this._fetch(url,{},'GET')
        this._update_page_info(pageNumber)
        this.make_render_request(this.template,next_page_items)
    },

    make_render_request(template,data){
        const content = renderToElement(template,{
            influencers: data,
            countries: countries,
            pagination_info: Array.from({ length: data.page_count }, (_, index) => index+1)
        })
        this.$target.html(content)
    },

      // Dropdown toggle method
    _onDropdownToggle(ev) {
        ev.stopPropagation();
        const $dropdown = $(ev.currentTarget).closest('.dropdown');
        const $dropdownContent = $dropdown.find('.dropdown-content');

        this.$target.find('.dropdown-content').not($dropdownContent).removeClass('show');

        $dropdownContent.toggleClass('show');
    },






    // Dropdown item selection method
    _onDropdownItemSelect(ev) {
        ev.preventDefault();
        const $item = $(ev.currentTarget);
        const $dropdown = $item.closest('.dropdown');
        const $dropdownBtn = $dropdown.find('.dropbtn');


        $dropdown.find('.dropdown-content').removeClass('show');
    },

_collectSearchParams(ev) {
        const searchParams = {
            // Get platform from custom select
            platform: this.$('.custom-select__option[data-type="platform"]')
                .filter((_, opt) => !$(opt).find('.tick-icon').hasClass('hidden'))
                .data('value') || 'instagram', // default to instagram if nothing selected

            // Gender radio buttons (keeping existing)
            gender: this.$('input[name="gender"]:checked').val(),

            // Country (assuming it's also a custom select, similar structure)
            country: this.$('.custom-select__option[data-type="country"]')
                .filter((_, opt) => !$(opt).find('.tick-icon').hasClass('hidden'))
                .data('value')
        };

        console.log('Collected Search Params:', searchParams);
        return searchParams;
    },


    // Close all dropdowns when clicking outside
    _closeDropdowns(ev) {
        if (!$(ev.target).closest('.dropdown').length) {
            this.$target.find('.dropdown-content').removeClass('show');
        }
    },

   async _render_search_influencer(ev) {
    ev.preventDefault();

    // Get search parameters
    const searchParams = this._collectSearchParams(ev);
    debugger

    try {
        // Fetch influencers with search parameters
        this.influencers = await this._get_influencers_data("/api/influencers", searchParams);
        this.currentPageNumber = 1;

        // Render results
        const content = renderToElement(this.template, {
            influencers: this.influencers,
            pagination_info: Array.from({ length: this.influencers.page_count }, (_, index) => index + 1),
            currentPageNumber: this.currentPageNumber
        });

        this.$target.html(content);
    } catch (error) {
        console.error('Search error:', error);
    }
},

});