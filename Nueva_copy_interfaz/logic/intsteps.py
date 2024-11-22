from sympy.integrals.manualintegrate import (AddRule, ConstantRule, ConstantTimesRule, DerivativeRule,
                                             DontKnowRule, ExpRule, TrigRule, PowerRule, RewriteRule,
                                             ArctanRule, PartsRule, TrigSubstitutionRule, URule, CyclicPartsRule)
from sympy import latex
import sympy as sp

def integral_steps_to_latex(step, level=0):
    if isinstance(step, AddRule):
        return integral_steps_to_latex(step.substeps[0], level + 1) + ['+'] + integral_steps_to_latex(step.substeps[1], level + 1)
    elif isinstance(step, ConstantRule):
        return [latex(step.constant)]
    elif isinstance(step, ConstantTimesRule):
        return [f'{latex(step.constant)} \\int {latex(step.other)} \\, d{latex(step.variable)}'] + integral_steps_to_latex(step.substep, level + 1)
    elif isinstance(step, DerivativeRule):
        return [latex(step.symbol)]
    elif isinstance(step, DontKnowRule):
        return [latex(step.integrand)]
    elif isinstance(step, ExpRule):
        base = latex(step.base)
        exp = latex(step.exp)
        return [f"{base}^{exp}"]
    elif isinstance(step, TrigRule):
        return [latex(step.symbol)]
    elif isinstance(step, PowerRule):
        base = latex(step.base)
        exp = latex(step.exp)
        new_exp = latex(step.exp + 1)
        return [f'\\int {base}^{exp} \\, d{latex(step.variable)} = \\frac{{{base}^{new_exp}}}{{{new_exp}}}']
    elif isinstance(step, RewriteRule):
        return integral_steps_to_latex(step.substep, level)
    elif isinstance(step, ArctanRule):
        return [latex(step.symbol)]
    elif isinstance(step, PartsRule):
        u = latex(step.u)  # Parte 'u' de integración por partes
        dv = latex(step.dv)  # Parte 'dv'
        
        # Verificar y procesar v_step
        if hasattr(step.v_step, "integrand"):
            v = latex(step.v_step.integrand)
            uv = latex(sp.Mul(step.u, step.v_step.integrand, evaluate=False))  # Evitar evaluación prematura
        else:
            v = latex(step.v_step)
            uv = latex(sp.Mul(step.u, sp.sympify(step.v_step), evaluate=False))
        
        # Procesar el segundo paso (sub-integral restante)
        if hasattr(step, "second_step"):
            integral_vdu = integral_steps_to_latex(step.second_step, level + 1)
        else:
            integral_vdu = ["\\text{No se encontró el segundo paso para completar la integración.}"]
        
        return [f"\\int {u} \\, {dv} = {uv} - \\int {v} \\, d{latex(step.variable)}"] + integral_vdu


    elif isinstance(step, TrigSubstitutionRule):
        return [latex(step.symbol)]
    elif isinstance(step, URule):
        return [f'\\int {latex(step.integrand)} \\, d{latex(step.symbol)} = \\int {latex(step.substep.integrand)} \\, d{latex(step.substep.variable)}'] + integral_steps_to_latex(step.substep, level + 1)
    elif isinstance(step, CyclicPartsRule):
        return integral_steps_to_latex(step.parts[0], level + 1) + ['and'] + integral_steps_to_latex(step.parts[1], level + 1)
    else:
        return [f'Unhandled step type: {type(step)}']

def integral_steps_to_latex_wrapper(step):
    latex_steps = integral_steps_to_latex(step, 0)
    # Filtrar los pasos irrelevantes y mantener solo las expresiones matemáticas
    filtered_steps = [step for step in latex_steps if not step.startswith('\\mathtt{\\text')]
    return filtered_steps

