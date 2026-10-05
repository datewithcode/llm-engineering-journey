import time

# ============================================
# EXAMPLE 1: return
# ============================================
print("=== EXAMPLE 1: return ===")
print()

def make_meal_return():
    time.sleep(1)   # pretend cooking takes time
    time.sleep(1)
    time.sleep(1)
    return "starter + main + dessert"

print("Calling the function...")
result = make_meal_return()
print(f"Got back: {result}")
print()
# Notice: you waited 3 seconds, then got everything at once.
# The variable 'result' now holds the value "starter + main + dessert"

input("Press Enter to see Example 2...")
print()

# ============================================
# EXAMPLE 2: print (NOT yield, NOT return)
# ============================================
print("=== EXAMPLE 2: print ===")
print()

def make_meal_print():
    time.sleep(1)
    print("starter")
    time.sleep(1)
    print("starter + main")
    time.sleep(1)
    print("starter + main + dessert")

print("Calling the function...")
result = make_meal_print()
print(f"Got back: {result}")
print()
# Notice: text appeared on screen one by one (good!)
# BUT result is None — the caller got NOTHING back.
# print talks to the screen, not to the caller.

input("Press Enter to see Example 3...")
print()

# ============================================
# EXAMPLE 3: yield
# ============================================
print("=== EXAMPLE 3: yield ===")
print()

def make_meal_yield():
    time.sleep(1)
    yield "starter"
    time.sleep(1)
    yield "starter + main"
    time.sleep(1)
    yield "starter + main + dessert"

print("Calling the function...")
for result in make_meal_yield():
    print(f"Got back: {result}")

print()
# Notice: text appeared one by one (like print)
# AND the caller got each value in 'result' (unlike print)
# The caller DECIDES what to do: print it, send to Gradio, save to file...

input("Press Enter to see the KEY difference...")
print()

# ============================================
# THE KEY DIFFERENCE
# ============================================
print("=== THE KEY DIFFERENCE ===")
print()
print("With RETURN:")
print("  result = make_meal_return()")
print(f"  result = '{make_meal_return()}'")
print(f"  The caller HAS the value. Can use it.")
print()

print("With PRINT:")
print("  result = make_meal_print()")
# This will print the meals again, ignore those
result_of_print = make_meal_print()
print(f"  result = {result_of_print}")
print(f"  The caller has NOTHING. None. The text went to the screen and vanished.")
print()

print("With YIELD:")
print("  for result in make_meal_yield():")
for r in make_meal_yield():
    print(f"    result = '{r}'  ← the caller has this, can send it anywhere")
print()

print("THAT is why Gradio needs yield, not print.")
print("Gradio is the caller. It needs to RECEIVE the text to show it on the UI.")
print("print sends text to your terminal. Gradio isn't watching your terminal.")
print("yield sends text to the caller (Gradio). Gradio shows it on the UI.")
