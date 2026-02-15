import os
import django
import re
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_django.settings')
django.setup()

from exams.models import Test, Question

def get_or_create_test():
    title = "Maths Revision 2 Phase 2"
    try:
        t = Test.objects.get(title=title)
        print(f"Found Test: {t.title}")
    except Test.DoesNotExist:
        print(f"Creating Test: {title}")
        t = Test.objects.create(
            title=title,
            description="Units 5-8",
            duration_minutes=90,
            has_compiler=False,
            is_active=True,
            scheduled_date=datetime.date.today()
        )
    return t

RAW_TEXT = """
The eccentricity of a parabola is
A) 0
B) 1
C) <1
D) >1
Answer: B

For ellipse, eccentricity e satisfies
A) e = 1
B) e > 1
C) 0 < e < 1
D) e = 0
Answer: C

Length of latus rectum of parabola y² = 4ax is
A) 2a
B) 4a
C) a
D) 8a
Answer: B

Director circle of x² + y² = a² is
A) x² + y² = 2a²
B) x² + y² = a²
C) x² + y² = 0
D) x² + y² = 4a²
Answer: C

Condition for line y = mx + c to be tangent to circle x² + y² = a² is
A) c = a
B) c² = a²(1+m²)
C) c² = a²
D) m² = 1
Answer: B

In hyperbola, transverse axis length is
A) 2a
B) 2b
C) a
D) b
Answer: A

Asymptotes of hyperbola x²/a² − y²/b² = 1 are
A) y = ±(b/a)x
B) y = ±(a/b)x
C) x = ±(a/b)y
D) x = ±(b/a)y
Answer: A

🔹 UNIT 6 – Vector Algebra

If a·b = 0, then vectors are
A) parallel
B) perpendicular
C) equal
D) collinear
Answer: B

Scalar triple product gives
A) area
B) length
C) volume
D) angle
Answer: C

If a × b = 0, then vectors are
A) perpendicular
B) parallel
C) unit
D) zero
Answer: B

Value of a·(b×c) equals volume of
A) rectangle
B) sphere
C) parallelepiped
D) triangle
Answer: C

Equation of plane in normal form is
A) ax+by+cz+d=0
B) r·n = d
C) x/a+y/b+z/c=1
D) ax+by+cz=0
Answer: B

Distance of point from plane is derived using
A) dot product
B) cross product
C) triple product
D) modulus
Answer: A

🔹 UNIT 7 – Differential Calculus

If f′(x) > 0 in interval, function is
A) decreasing
B) constant
C) increasing
D) zero
Answer: C

Condition for local maxima is
A) f′=0, f″>0
B) f′=0, f″<0
C) f′≠0
D) f″=0
Answer: B

Point of inflection occurs when
A) f′=0
B) f″ changes sign
C) f″=0 only
D) f′ changes sign
Answer: B

Radius of curvature is inverse of
A) slope
B) curvature
C) tangent
D) secant
Answer: B

Taylor’s series expansion requires function to be
A) continuous
B) differentiable sufficiently
C) bounded
D) periodic
Answer: B

🔹 UNIT 8 – Partial Derivatives

∂f/∂x treats other variables as
A) zero
B) constant
C) variable
D) infinity
Answer: B

Total differential of z = f(x,y) is
A) dz = fx dx
B) dz = fy dy
C) dz = fx dx + fy dy
D) dz = 0
Answer: C

If fx = fy = 0 at point, it is
A) maximum
B) minimum
C) stationary point
D) asymptote
Answer: C

Jacobian represents
A) determinant
B) slope
C) limit
D) area
Answer: A

Chain rule applies when
A) independent variables
B) composite functions
C) linear functions
D) constants
Answer: B

In ellipse, sum of focal distances is
A) 2b
B) 2c
C) 2a
D) a
Answer: C

Angle between vectors a and b is found using
A) cross product
B) dot product
C) scalar triple
D) modulus only
Answer: B

Increasing function implies
A) f′<0
B) f′=0
C) f′>0
D) f″>0
Answer: C

If Hessian determinant >0 and fxx>0 →
A) maximum
B) minimum
C) saddle
D) none
Answer: B

Equation of tangent to parabola y²=4ax at (x1,y1) is
A) yy1=2a(x+x1)
B) yy1=2a(x−x1)
C) yy1=2a(x+x1)
D) y y1 = 2a(x + x1)
Answer: D

Magnitude of cross product equals
A) |a||b|cosθ
B) |a||b|sinθ
C) |a||b|
D) 1
Answer: B

Divergence of vector field measures
A) rotation
B) spreading
C) length
D) area
Answer: B

🔥 PART B – BOOK BACK EXERCISE MCQs (30)

Equation of normal to circle x²+y²=a² at (x1,y1) is
A) xx1+yy1=a²
B) y−y1=m(x−x1)
C) x/x1=y/y1
D) x x1 + y y1 = a²
Answer: D

If vectors are unit and perpendicular, dot product is
A) 1
B) −1
C) 0
D) 2
Answer: C

Maximum area of rectangle under parabola occurs at
A) endpoint
B) vertex
C) origin
D) focus
Answer: B

Reduction formula decreases power by
A) 2
B) 1
C) 3
D) none
Answer: A

Gradient vector is perpendicular to
A) tangent
B) normal
C) level surface
D) axis
Answer: C

If determinant of Jacobian ≠ 0 →
A) dependent
B) independent
C) constant
D) zero
Answer: B

Condition for tangent to hyperbola is
A) c²=a²+b²
B) c²=a²−b²
C) c²=b²−a²
D) c²=ab
Answer: B

If f′ changes from + to − →
A) minimum
B) maximum
C) inflection
D) none
Answer: B

Area of parallelogram formed by a,b equals
A) a·b
B) |a×b|
C) |a|+|b|
D) 0
Answer: B

Stationary point occurs when
A) f′=1
B) f′=0
C) f″=0
D) f=0
Answer: B

Directrix of parabola y²=4ax is x=
A) a
B) −a
C) 2a
D) −2a
Answer: B

If |a|=|b| and a·b=|a||b| → angle is
A) 0°
B) 90°
C) 180°
D) 45°
Answer: A

If second derivative >0 → curve is
A) concave up
B) concave down
C) linear
D) constant
Answer: A

Partial derivative of constant is
A) 1
B) 0
C) x
D) y
Answer: B

Asymptotes of rectangular hyperbola are
A) axes
B) diagonals
C) tangents
D) normals
Answer: A

If scalar triple product = 0 → vectors are
A) perpendicular
B) coplanar
C) parallel
D) equal
Answer: B

Increasing & concave down →
A) max
B) min
C) flattening
D) none
Answer: C

Condition for extremum in two variables →
A) fx=0 only
B) fy=0 only
C) fx=fy=0
D) fxx=0
Answer: C

Centre of ellipse x²/a²+y²/b²=1 is
A) (a,b)
B) (0,0)
C) (a,0)
D) (0,b)
Answer: B

Eccentricity of hyperbola >
A) 0
B) 1
C) 2
D) ∞
Answer: B

Unit normal vector magnitude =
A) 0
B) 1
C) 2
D) a
Answer: B

Inflection point condition
A) f″=0 & sign change
B) f′=0
C) f=0
D) none
Answer: A

Level curve equation obtained by
A) f(x,y)=c
B) f′=0
C) ∂f=0
D) none
Answer: A

Vertex of parabola y²=4ax is
A) (a,0)
B) (0,a)
C) (0,0)
D) (−a,0)
Answer: C

If |a×b|=0 →
A) perpendicular
B) parallel
C) equal
D) zero vectors only
Answer: B

Monotonic decreasing →
A) f′>0
B) f′<0
C) f″>0
D) none
Answer: B

Total differential approximates
A) exact value
B) small change
C) constant
D) none
Answer: B

Tangent slope equals
A) dy/dx
B) dx/dy
C) y/x
D) constant
Answer: A

Volume using triple product formula =
A) |a·(b×c)|
B) |a×b|
C) a·b
D) |a|
Answer: A

Hessian <0 indicates
A) minimum
B) maximum
C) saddle
D) none
Answer: C
"""

def parse_and_add():
    test = get_or_create_test()
    
    # Update date for today exam
    test.scheduled_date = datetime.date.today()
    test.is_active = True
    test.save()
    print(f"Test scheduled for TODAY: {test.scheduled_date}")

    # Clearing existing questions? 
    # User said add 60 questions. It's safer to clear to avoid confusion if older incomplete qs exist.
    count_existing = test.questions.count()
    if count_existing > 0:
        print(f"Clearing {count_existing} existing questions...")
        test.questions.all().delete()
        
    lines = RAW_TEXT.split('\n')
    current_q_text = ""
    current_options = []
    current_cat = "General"
    questions_added = 0
    
    # Regex for options A) ... or A. ...
    opt_pat = re.compile(r'^[A-D]\)\s*(.*)') 
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect Category Header
        if "UNIT" in line or "PART B" in line:
            if "UNIT 6" in line: current_cat = "Vector Algebra"
            elif "UNIT 7" in line: current_cat = "Differential Calculus"
            elif "UNIT 8" in line: current_cat = "Partial Derivatives"
            elif "PART B" in line: current_cat = "Book Back MCQs"
            continue
            
        # Ignore filler lines
        if "similarly included" in line or "Continuing inside questions" in line or "following same difficulty" in line:
            continue

        # Check for Answer
        if line.startswith("Answer:"):
            # End of question block
            ans_char = line.replace("Answer:", "").strip()
            # Map char to full answer string if possible, OR just store char?
            # My system usually stores full string text as correct_answer.
            # Convert char to option text
            valid_opts = ["A", "B", "C", "D"]
            correct_text = ans_char
            
            # Find matching option text
            if ans_char in valid_opts and len(current_options) >= valid_opts.index(ans_char)+1:
                idx = valid_opts.index(ans_char)
                correct_text = current_options[idx]
                
            if current_q_text and current_options:
                Question.objects.create(
                    test=test,
                    text=current_q_text,
                    options=current_options,
                    correct_answer=correct_text,
                    category=current_cat,
                    difficulty="Medium",
                    type="mcq"
                )
                questions_added += 1
                # print(f"Added Q: {current_q_text[:30]}...")
            
            # Reset
            current_q_text = ""
            current_options = []
            continue
            
        # Check for Option
        match = opt_pat.match(line)
        if match:
            opt_text = match.group(1).strip()
            # Handle symbols if needed
            current_options.append(opt_text)
            continue
            
        # Else it's question text
        # If we already have options but no answer yet?
        if current_options:
            # Maybe multiline option? Ignore for now, assume single line options.
            continue
            
        current_q_text += line + " "

    print(f"Successfully added {questions_added} questions to '{test.title}'")

if __name__ == "__main__":
    parse_and_add()
