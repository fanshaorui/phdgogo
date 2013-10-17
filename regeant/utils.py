# -*- coding: utf-8 -*-


class Pagination(object):

    """ Pagination object for search result pagination.
        This is a helper class, modifiedy from flask-SQLAlchemy.
        This class has almost the same interface.
        @author: kid143
        @version: 0.0.1
        @since: 1.0
    """

    def __init__(self, search_query, pagenum, per_page=20):
        # The sphinx search query object contains result set,
        # so we don't need items object or list
        self._query = search_query
        # current page number
        self.pagenum = pagenum
        # number of results displayed in one page
        self.per_page = per_page
        # total number of results
        self.total = search_query.count()

    @property
    def pages(self):

        """The total number of pages of the results."""

        return int(ceil(self.total/float(self.pagenum)))

    def prev(self):

        """Returns a :class: `Pagination` object representing the
           previous page.
        """

        assert self._query is not None, 'query needed.'
        return self.__class__(
            self._query, self.prev_num, self.per_page, self.total)

    @property
    def prev_num(self):

        """Number of the previous page."""

        return self.pagenum - 1

    @property
    def has_prev(self):

        """True if a previous page exists."""

        return self.pagenum > 1

    @property
    def next(self):

        """Returns a :class: `Pagenation` object for the next page."""

        assert self._query is not None, 'query needed.'
        return self.__class__(
            self._query, self.next_num, self.per_page, self.total)

    @property
    def has_next(self):

        """True if a next page exists."""

        return self.pagenum < self.pages

    @property
    def next_num(self):

        """Number of the next page."""

        return self.pagenum + 1

    @property
    def iter_pages(
        self, left_edge=2, left_current=2,
        right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """

        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
                (num > self.pagenum - left_current -1 and \
                    num < self.pagenum + right_current) or \
                num > self.pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

    @property
    def cur_page(self):

        """Returns search results of current page."""

        page_end = self.pagenum * self.per_page - 1
        page_start = page_end - self.per_page + 1
        return self._query[page_start:page_end]
