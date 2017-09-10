
HEAD = '''
<!DOCTYPE html>
<html lang="en">
        <head>
                <meta charset="utf-8">
                <title>Tin tức Python HackerNews — hn.PyMI.vn</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <meta name="description" content="Tin tức mới nhất về Python - học lập trình Python căn bản và nâng cao - đào tạo học viên từ không biết gì thành lập trình viên chuyên nghiệp." />
                <meta name="keywords" content="python, hoc python, hoc lap trinh python, hoc lap trinh, tai liey python, lap trinh python,
                lap trinh, hoc lap trinh, học python, học lập trình python, tài liêu python, học lập trình,
                hoc django, học django, tai lieu django, pyjobs, pyfml, python viet nam, python vietnam, pymi" />
                <meta name="author" content="http://pymi.vn" />


                <style>
            table, th, td {
                border: 1px solid black;
            }
            th {
                color: chocolate;
            }
                </style>

                <script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-15373673-8', 'auto');
ga('send', 'pageview');

                </script>

        </head>
        <body>
                <h1 style="color:#66A8CD;">Tin tức Python HackerNews - hn.PyMI.vn</h1>
                <h3 style="color:#FFDE56;">Các tin tức tuyển chọn - HOT (><a href="https://en.wikipedia.org/wiki/42_(number)#The_Hitchhiker.27s_Guide_to_the_Galaxy" target="_blank">42</a> score)</h3>

<ul>
'''

TAIL = '''
</ul>

        <footer>
	    <br/>Đăng ký học lập trình Python tại <a href="https://pymi.vn">PyMivn</a>
            <br/>Học lập trình Python chất lượng số 1 Việt Nam © 2017.
            <br/>Tự học thì <a href="http://pymi.vn/tutorial/">bấm vào đây nhé ;)</a>
            <br/>Rendered at {time} GMT+7.
        </footer>

</body></html>
'''

LINE = '<li><a href="{url}" target="_blank">{title}</a> - <a href="{hn_url}" target="_blank">comment</a></li>\n'
