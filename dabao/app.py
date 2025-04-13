from flask import Flask, render_template_string, request, session
import ast

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个密钥用于会话加密

@app.route('/', methods=['GET', 'POST'])
def calculator():
    # 从会话中获取表达式，如果没有则初始化为空字符串
    expression = session.get('expression', "")
    result = None
    if request.method == 'POST':
        button = request.form.get('button')
        if button is not None:
            if button == '=':
                try:
                    # 尝试解析表达式
                    ast.parse(expression)
                    # 执行表达式
                    result = eval(expression)
                except SyntaxError:
                    result = "语法错误，请检查输入"
                except ZeroDivisionError:
                    result = "错误：除数不能为零"
                except Exception as e:
                    result = f"未知错误：{str(e)}"
            elif button == 'C':
                expression = ""
            else:
                expression += button
        # 更新会话中的表达式
        session['expression'] = expression

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" rel="stylesheet">
    <title>计算器</title>
</head>
<body class="bg-gray-200 flex justify-center items-center h-screen">
    <div class="bg-white p-4 rounded-lg shadow-lg w-80">
        <div class="text-center text-2xl font-bold mb-4">高级计算器</div>
        <form method="post">
            <input type="text" name="expression" value="{{ expression }}" class="w-full p-3 mb-3 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-right" readonly>
            <div class="grid grid-cols-4 gap-3 mb-4">
                <button type="submit" name="button" value="7" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">7</button>
                <button type="submit" name="button" value="8" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">8</button>
                <button type="submit" name="button" value="9" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">9</button>
                <button type="submit" name="button" value="/" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">/</button>
                <button type="submit" name="button" value="4" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">4</button>
                <button type="submit" name="button" value="5" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">5</button>
                <button type="submit" name="button" value="6" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">6</button>
                <button type="submit" name="button" value="*" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">*</button>
                <button type="submit" name="button" value="1" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">1</button>
                <button type="submit" name="button" value="2" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">2</button>
                <button type="submit" name="button" value="3" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">3</button>
                <button type="submit" name="button" value="-" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">-</button>
                <button type="submit" name="button" value="0" class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">0</button>
                <button type="submit" name="button" value="." class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-md">.</button>
                <button type="submit" name="button" value="=" class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-4 rounded-md">=</button>
                <button type="submit" name="button" value="+" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">+</button>
                <button type="submit" name="button" value="&" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">&</button>
                <button type="submit" name="button" value="|" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">|</button>
                <button type="submit" name="button" value="~" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">~</button>
                <button type="submit" name="button" value="^" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md">^</button>
                <button type="submit" name="button" value="C" class="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-4 rounded-md col-span-2">C</button>
            </div>
        </form>
        {% if result is not none %}
        <div class="bg-gray-100 p-3 rounded-md text-center text-lg font-bold">
            结果: {{ result }}
        </div>
        {% endif %}
    </div>
</body>
</html>
    """
    return render_template_string(html_template, expression=expression, result=result)

if __name__ == '__main__':
    app.run(debug=True)