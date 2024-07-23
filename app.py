from flask import Flask, request, jsonify, render_template
from functools import reduce
from math import gcd as math_gcd
from fractions import Fraction
from scipy.special import gamma
from sympy import sympify, Rational
import re

def create_app():
    app = Flask(__name__)






    # Function to calculate the LCM of two integers
    def lcm_of_two(a, b):
        return abs(a * b) // math_gcd(a, b)


    # Function to calculate the LCM of a list of integers
    def calculate_lcm(numbers):
        return reduce(lcm_of_two, numbers)

    # Function to calculate the LCM of fractions
    def lcm_of_fractions(fracs):
        numerators = [frac.numerator for frac in fracs]
        denominators = [frac.denominator for frac in fracs]
        lcm_numer = calculate_lcm(numerators)
        gcd_denom = reduce(math_gcd, denominators)
        return Fraction(lcm_numer, gcd_denom)



    # Function to calculate the HCF of fractions
    def hcf_of_fractions(fracs):
        numerators = [frac.numerator for frac in fracs]
        denominators = [frac.denominator for frac in fracs]
        gcd_numer = reduce(math_gcd, numerators)
        lcm_denom = calculate_lcm(denominators)
        return Fraction(gcd_numer, lcm_denom)


    # Function to calculate the factorial using the Gamma function
    def factorial_of_fraction(number):
        if number < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        return gamma(float(number) + 1)









    #ALL ROUTES:

    @app.route('/')
    def index():
        return render_template('index.html')



    # ADDITION

    @app.route('/addition')
    def addition_page():
        return render_template('addition.html')

    @app.route('/api/calculate_addition', methods=['POST'])
    def api_calculate_addition():
        data = request.json
        try:
            numbers = [Fraction(num) for num in data['numbers']]
            result = sum(numbers)
            return jsonify({'result': str(result)})
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400


    # SUBTRACTION
    @app.route('/subtraction')
    def subtraction_page():
        return render_template('subtraction.html')


    @app.route('/api/calculate_subtraction', methods=['POST'])
    def api_calculate_subtraction():
        data = request.json
        try:
            numbers = [Fraction(num) for num in data['numbers']]
            result = reduce(lambda x, y: x - y, numbers)
            return jsonify({'result': str(result)})
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400



    # MULTIPLICATION
    @app.route('/multiplication')
    def multiplication_page():
        return render_template('multiplication.html')

    @app.route('/api/calculate_multiplication', methods=['POST'])
    def api_calculate_multiplication():
        data = request.json
        try:
            numbers = [Fraction(num) for num in data['numbers']]
            result = reduce(lambda x, y: x * y, numbers)
            return jsonify({'result': str(result)})
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400




    #DIVISION
    @app.route('/division')
    def division_page():
        return render_template('division.html')

    @app.route('/api/calculate_division', methods=['POST'])
    def api_calculate_division():
        data = request.json
        try:
            numbers = [Fraction(num) for num in data['numbers']]
            
            # Check if there are any zeros in the list
            if 0 in numbers[1:]:
                return jsonify({'error': 'Division by zero is not defined.'}), 400
            
            # Calculate the result using reduce
            result = reduce(lambda x, y: x / y, numbers)
            
            # Check if the result is valid
            if result.denominator == 0:
                return jsonify({'error': 'Resulting division is undefined (0/0).'}), 400
            
            return jsonify({'result_fraction': str(result), 'result_decimal': float(result)})
        except ZeroDivisionError:
            return jsonify({'error': 'Division by zero encountered.'}), 400
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400



    # BODMAS
    @app.route('/bodmas')
    def bodmas_page():
        return render_template('bodmas.html')

    @app.route('/api/calculate_bodmas', methods=['POST'])
    def api_calculate_bodmas():
        data = request.json
        expression = data.get('expression')
        
        try:
            # Replace fractions in the expression with their Rational equivalent
            fraction_pattern = re.compile(r'(\d+/\d+)')
            fractions = fraction_pattern.findall(expression)
            
            for frac in fractions:
                frac_obj = Rational(frac)
                expression = expression.replace(frac, f"({frac_obj})")
            
            # Evaluate the expression safely using sympy
            result = sympify(expression)
            
            # Convert the result to a fraction and decimal
            result_fraction = result if isinstance(result, Rational) else Rational(result)
            result_decimal = float(result_fraction)
            
            return jsonify({'result_fraction': str(result_fraction), 'result_decimal': result_decimal})
        
        except ZeroDivisionError:
            return jsonify({'error': 'Division by zero encountered.'}), 400
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter a valid expression.'}), 400



    # LCM

    @app.route('/lcm')
    def lcm_page():
        return render_template('lcm.html')

    @app.route('/api/calculate_lcm', methods=['POST'])
    def api_calculate_lcm():
        data = request.json
        try:
            numbers = [Fraction(num) for num in data['numbers']]
            lcm_result = lcm_of_fractions(numbers)
            return jsonify({'lcm': str(lcm_result)})
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400



    #HCF

    @app.route('/hcf')
    def hcf_page():
        return render_template('hcf.html')

    @app.route('/api/calculate_hcf', methods=['POST'])
    def api_calculate_hcf():
        data = request.json
        try:
            numbers = [Fraction(num) for num in data['numbers']]
            hcf_result = hcf_of_fractions(numbers)
            return jsonify({'hcf': str(hcf_result)})
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400



    # FACTORIAL

    @app.route('/factorial')
    def factorial_page():
        return render_template('factorial.html')


    @app.route('/api/calculate_factorial', methods=['POST'])
    def api_calculate_factorial():
        data = request.json
        try:
            number = Fraction(data['number'])
            factorial_result = factorial_of_fraction(number)
            return jsonify({'factorial': float(factorial_result)})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Invalid input. Please enter a valid number.'}), 400


    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
