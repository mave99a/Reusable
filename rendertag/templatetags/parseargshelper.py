def parse_args_kwargs_and_as_var(parser, bits):
    args = []
    kwargs = {}
    as_var = None
    
    bits = iter(bits)
    for bit in bits:
        if bit == 'as':
            as_var = bits.next()
            break
        else:
            for arg in bit.split(","):
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    k = k.strip()
                    kwargs[k] = v
                elif arg:
                    args.append(arg)
    return args, kwargs, as_var
