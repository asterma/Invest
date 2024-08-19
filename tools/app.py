from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def calculate_return_on_investment(
    house_price, down_payment_ratio, interest_rate, monthly_rent
):
    # 计算首付金额，包括额外的11.5%购房成本
    initial_down_payment = house_price * down_payment_ratio
    additional_costs = house_price * 0.11
    total_down_payment = initial_down_payment + additional_costs

    # 计算总购买成本
    total_cost = house_price * 1.11

    # 计算贷款本金
    loan_amount = total_cost - initial_down_payment

    # 转换年利率为月利率
    monthly_interest_rate = interest_rate / 12

    # 假设贷款期限为30年（360个月）
    loan_term_months = 30 * 12

    # 计算每月还款额
    monthly_payment = (
        loan_amount
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months)
        / ((1 + monthly_interest_rate) ** loan_term_months - 1)
    )

    # 初始化贷款余额
    current_balance = loan_amount
    annual_interest_payment = 0

    # 计算一年内的利息支出
    for month in range(12):
        interest_payment = current_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        annual_interest_payment += interest_payment
        current_balance -= principal_payment

    # 计算年收入
    annual_rent_income = monthly_rent * 12

    # 计算净年收益
    net_annual_profit = annual_rent_income - annual_interest_payment

    # 计算收益率（净年收益 / 总首付金额）
    return_on_investment = net_annual_profit / total_down_payment

    return (
        total_down_payment,
        monthly_payment,
        return_on_investment * 100,
    )  # 将收益率转换为百分比


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    house_price = float(data["house_price"])
    down_payment_ratio = float(data["down_payment_ratio"])
    interest_rate = float(data["interest_rate"])
    monthly_rent = float(data["monthly_rent"])

    total_down_payment, monthly_payment, roi = calculate_return_on_investment(
        house_price, down_payment_ratio, interest_rate, monthly_rent
    )

    return jsonify(
        {
            "total_down_payment": total_down_payment,
            "monthly_payment": monthly_payment,
            "roi": roi,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
