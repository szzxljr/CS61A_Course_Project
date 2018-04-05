class Procedure:
    """The supertype of all Scheme procedures."""
    def eval_call(self, operands, env):
        """Standard function-call evaluation on SELF with OPERANDS as the
        unevaluated actual-parameter expressions and ENV as the environment
        in which the operands are to be evaluated."""
        # BEGIN PROBLEM 5
        args = operands.map(lambda expr : scheme_eval(expr, env))
        return scheme_apply(self, args, env)
        # END PROBLEM 5

def do_define_form(expressions, env):
    """Evaluate a define form."""
    check_form(expressions, 2)
    target = expressions.first
    if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        # BEGIN PROBLEM 6
        env.define(target, scheme_eval(expressions.second.first, env))
        return target
        # END PROBLEM 6
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN PROBLEM 10
        formals = target.second
        target = target.first
        body = expressions.second
        env.define(target, do_lambda_form(Pair(formals, body), env))
        return target
        # END PROBLEM 10
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))

        

def do_define_macro(expressions, env):
    """Evaluate a define-macro form."""
    # BEGIN Problem 21
    check_form(expressions, 2)
    target = expressions.first
    '''if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        # BEGIN PROBLEM 6
        env.define(target, scheme_eval(expressions.second.first,env))
        return target
        # END PROBLEM 6'''
    if isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN PROBLEM 10
        procedure = MacroProcedure(target.second, expressions.second, env)
        env.define(target.first, procedure)
        return target.first
        # END PROBLEM 10
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))
    # END Problem 21 

class MacroProcedure(LambdaProcedure):
    """A macro: a special form that operates on its unevaluated operands to
    create an expression that is evaluated in place of a call."""

    def eval_call(self, operands, env):
        """Macro call evaluation on me with OPERANDS as the unevaluated
        actual-parameter expressions and ENV as the environment in which the
        resulting expanded expression is to be evaluated."""
        # BEGIN Problem 21
        args = operands.map(lambda x: complete_eval(x))
        return scheme_apply(self, args, env)
        # END Problem 21