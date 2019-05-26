# __author: iamironman


class Pagination(object):
    def __init__(self, request, current_page, all_data, per_page_num=2, max_page_count=11):
        try:
            current_page = int(current_page)
        except Exception:
            current_page = 1
        if current_page < 1:
            current_page = 1
        self.current_page = current_page
        self.all_count = len(all_data)
        self.per_page_num = per_page_num
        all_pager, tmp = divmod(self.all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager
        self.max_page_count = max_page_count
        self.max_page_count_half = int((max_page_count - 1) / 2)
        self.request = request
        import copy
        self.params = copy.deepcopy(self.request.GET)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        if self.all_pager <= self.max_page_count:
            page_range = range(1, self.all_pager + 1)
        else:
            if self.current_page <= self.max_page_count_half:
                page_range = range(1, self.max_page_count + 1)
            else:
                if (self.current_page + self.max_page_count_half) > self.all_pager:
                    page_range = range(self.all_pager - self.max_page_count + 1, self.all_pager + 1)
                else:
                    page_range = range(self.current_page - self.max_page_count_half,
                                       self.current_page + self.max_page_count_half + 1)
        page_html_list = []
        self.params['page'] = 1
        first_page = "<nav aria-label='Page navigation'><ul class='pagination'><li><a href='?{}'>首页</a></li>".format(
            self.params.urlencode(),
        )
        page_html_list.append(first_page)
        self.params['page'] = self.current_page - 1
        if self.current_page <= 1:
            prev_page = "<li class='disabled'><a href='#'>上一页</a></li>"
        else:
            prev_page = "<li><a href='?{}'>上一页</a></li>".format(self.params.urlencode(), )
        page_html_list.append(prev_page)
        for i in page_range:
            self.params['page'] = i
            if i == self.current_page:
                temp = "<li class='active'><a href='?{}'>{}</a></li>".format(self.params.urlencode(), i, )
            else:
                temp = "<li><a href='?{}'>{}</a></li>".format(self.params.urlencode(), i, )
            page_html_list.append(temp)
        self.params['page'] = self.current_page + 1
        if self.current_page >= self.all_pager:
            next_page = "<li class='disabled'><a href='#'>下一页</a></li>"
        else:
            next_page = "<li><a href='?{}'>下一页</a></li>".format(self.params.urlencode(), )
        page_html_list.append(next_page)
        self.params['page'] = self.all_pager
        last_page = "<li><a href='?{}'>尾页</a></li></ul></nav>".format(self.params.urlencode())
        page_html_list.append(last_page)
        return ''.join(page_html_list)
