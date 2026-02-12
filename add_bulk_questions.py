import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_django.settings')
django.setup()

from exams.models import Test, Question

TEST_ID = 7

DATA = """
1. If A is singular, then
A) A⁻¹ exists
B) adj A = O
C) ∣A∣ = 0
D) rank A = n
Answer: C

2. If A is a non-singular matrix, then
A) adj A = 0
B) A⁻¹ = 1/∣A∣
C) A⁻¹ = (1/∣A∣) adj A
D) Aᵀ = A⁻¹
Answer: C

3. If AB=AC and A is non-singular, then
A) B ≠ C
B) B = C
C) A = 0
D) C = 0
Answer: B

4. If ∣A∣ = 1, then ∣A⁻¹∣ equals
A) 0
B) −1
C) 1
D) ∞
Answer: C

5. If A is orthogonal, then
A) Aᵀ = A
B) A⁻¹ = Aᵀ
C) ∣A∣ = 0
D) adj A = A
Answer: B

6. If z + z̄ = 0, then z is
A) real
B) purely imaginary
C) complex
D) zero
Answer: B

7. If ∣z∣ = 1, then z z̄ equals
A) −1
B) 0
C) 1
D) i
Answer: C

8. The locus of z such that ∣z−3∣=∣z+3∣ is
A) circle
B) parabola
C) imaginary axis
D) straight line
Answer: C

9. Argument of a negative real number is
A) 0
B) π
C) π/2
D) −π/2
Answer: B

10. If zⁿ=1, the roots lie on
A) imaginary axis
B) real axis
C) unit circle
D) parabola
Answer: C

11. Sum of roots of ax² + bx + c = 0 equals
A) c/a
B) b/a
C) −b/a
D) −c/a
Answer: C

12. If one root is reciprocal of the other, then
A) c=a
B) b=0
C) a=0
D) c=0
Answer: A

13. If roots are equal, discriminant is
A) positive
B) negative
C) zero
D) infinity
Answer: C

14. Number of positive roots is given by
A) Rolle’s rule
B) Descartes’ rule
C) Vieta’s rule
D) Newton’s rule
Answer: B

15. If all coefficients are real, complex roots occur in
A) pairs
B) triples
C) single
D) none
Answer: A

16. Domain of sin⁻¹ x is
A) ℝ
B) (−∞,∞)
C) [−1,1]
D) (0,1)
Answer: C

17. Principal value of tan⁻¹ x lies in
A) [0,π]
B) (−π/2,π/2)
C) (0,π/2)
D) (−π,π)
Answer: B

18. sin⁻¹(sin 5π/6) equals
A) 5π/6
B) π/6
C) −π/6
D) −5π/6
Answer: B

19. cos⁻¹x + sin⁻¹x =
A) π
B) 0
C) π/2
D) −π/2
Answer: C

20. tan⁻¹1 + tan⁻¹2 + tan⁻¹3 =
A) π/2
B) π
C) 0
D) 3π/2
Answer: B

21. Rank of identity matrix of order n is
A) 0
B) 1
C) n
D) n²
Answer: C

22. A matrix is invertible if and only if it is
A) square
B) symmetric
C) non-singular
D) diagonal
Answer: C

23. For any square matrix A, adj(adj A) equals
A) A
B) |A|A
C) |A|ⁿ⁻² A
D) |A|²A
Answer: C

24. If z=reⁱᶿ, then r represents
A) argument
B) imaginary part
C) modulus
D) conjugate
Answer: C

25. Euler’s formula connects
A) algebra and geometry
B) trigonometry and calculus
C) exponential and trigonometric functions
D) matrices and vectors
Answer: C

26. The number of nth roots of unity is
A) n−1
B) n
C) 2n
D) infinite
Answer: B

27. Nature of roots depends on
A) coefficient a
B) constant term
C) discriminant
D) degree
Answer: C

28. If α, β are roots, then polynomial with roots α², β² is obtained by
A) substitution
B) squaring equation
C) elimination
D) division
Answer: C

29. Principal value branch ensures inverse trig function is
A) continuous
B) one-one
C) periodic
D) bounded
Answer: B

30. sin⁻¹ x is defined only when
A) x ∈ ℝ
B) |x| ≥ 1
C) |x| ≤ 1
D) x > 0
Answer: C

31. If A is symmetric, then adj A is
A) skew-symmetric
B) diagonal
C) symmetric
D) orthogonal
Answer: C

32. The locus of ∣z∣=r represents
A) straight line
B) circle
C) parabola
D) ellipse
Answer: B

33. If roots are real and distinct, discriminant is
A) zero
B) negative
C) positive
D) imaginary
Answer: C

34. Domain of cos⁻¹ x is
A) ℝ
B) (−∞,∞)
C) [−1,1]
D) (0,π)
Answer: C

35. Range of cos⁻¹ x is
A) (−π/2,π/2)
B) [0,π]
C) (−π,π)
D) ℝ
Answer: B

36. If α is a root, then −α is also a root when polynomial has
A) even powers only
B) odd powers only
C) mixed powers
D) constant term zero
Answer: A

37. Conjugate of a + ib is
A) a + ib
B) a − ib
C) −a + ib
D) −a − ib
Answer: B

38. Matrix used in rotation in geometry is
A) diagonal
B) orthogonal
C) singular
D) triangular
Answer: B

39. If A is singular, then
A) adj A ≠ 0
B) A⁻¹ exists
C) ∣A∣ = 0
D) rank is full
Answer: C

40. Principal value of sin⁻¹ x lies in
A) (−π,π)
B) (−π/2,π/2)
C) [0,π]
D) ℝ
Answer: B

41. If A is a square matrix such that A²=I, then A⁻¹ is
A) A²
B) A
C) −A
D) I
Answer: B

42. If ∣A∣ = −2, then ∣2A∣ for a 3×3 matrix is
A) −4
B) −8
C) −16
D) −32
Answer: D

43. If A is skew-symmetric of odd order, then ∣A∣ equals
A) 1
B) −1
C) 0
D) undefined
Answer: C

44. Rank of a zero matrix is
A) 1
B) n
C) undefined
D) 0
Answer: D

45. If AB=O and A≠O, then
A) B=O always
B) B may be non-zero
C) A is singular
D) B is identity
Answer: B

46. If z = a + ib and ∣z∣ = 0, then
A) a=0
B) b=0
C) a=b=0
D) z=i
Answer: C

47. The geometric representation of a purely imaginary number is a point on
A) x-axis
B) y-axis
C) origin
D) unit circle
Answer: B

48. If z z̄ = 25, then ∣z∣ equals
A) 5
B) −5
C) 25
D) ±5
Answer: A

49. If z = cos θ + i sin θ, then ∣z∣ is
A) cos θ
B) sin θ
C) θ
D) 1
Answer: D

50. The locus of points satisfying ∣z−i∣ = ∣z+i∣ is
A) x-axis
B) y-axis
C) circle
D) parabola
Answer: A

51. If the roots of a quadratic equation are equal, then the graph of the equation
A) cuts x-axis at two points
B) does not touch x-axis
C) touches x-axis at one point
D) is parallel to x-axis
Answer: C

52. If sum and product of roots are both zero, then roots are
A) 1, −1
B) 0, 0
C) 1, 0
D) −1, 0
Answer: B

53. The maximum number of real roots of a polynomial of degree n is
A) n−1
B) n
C) 2n
D) infinite
Answer: B

54. If a polynomial has only even powers of x, then
A) roots are equal
B) roots are imaginary
C) roots occur in pairs ±α
D) roots are zero
Answer: C

55. Descartes’ rule of signs gives information about
A) exact roots
B) imaginary roots
C) positive and negative roots
D) rational roots
Answer: C

56. sin⁻¹(−x) equals
A) sin⁻¹ x
B) −sin⁻¹ x
C) π − sin⁻¹ x
D) π + sin⁻¹ x
Answer: B

57. cos⁻¹(−x) equals
A) cos⁻¹ x
B) π − cos⁻¹ x
C) −cos⁻¹ x
D) π + cos⁻¹ x
Answer: B

58. tan⁻¹(−x) equals
A) tan⁻¹ x
B) −tan⁻¹ x
C) π − tan⁻¹ x
D) π + tan⁻¹ x
Answer: B

59. The range of sin⁻¹ x is chosen to make it
A) periodic
B) bounded
C) continuous
D) one-one
Answer: D

60. tan⁻¹1 + tan⁻¹2 + tan⁻¹3 equals
A) π/2
B) π
C) 3π/2
D) 0
Answer: B
"""

def parse_and_add():
    # Remove existing
    # Remove existing
    try:
        test = Test.objects.get(title="Maths Revision 2 Phase 1")
    except Test.DoesNotExist:
        print("Test 'Maths Revision 2 Phase 1' not found. Please run seed_full.py first.")
        return

    print(f"Adding questions to: {test.title} (ID: {test.id})")
    
    # Split by double newline usually separates questions
    # But user input has varied spacing.
    # But each question ends with "Answer: X".
    
    parts = re.split(r'Answer: ([A-D])', DATA)
    print(f"Split into {len(parts)} parts.")
    
    count = 0
    for i in range(0, len(parts)-1, 2):
        block = parts[i].strip()
        ans_char = parts[i+1].strip()
        
        if not block: continue
        
        # Parse block options using search from end
        # Format: Question\nA) ...\nB) ...
        # Regex: Look for A) ... at the end
        m = re.search(r'(.*?)\nA\) (.*)\nB\) (.*)\nC\) (.*)\nD\) (.*)', block, re.DOTALL)
        
        if m:
            q_text = m.group(1).strip()
            q_text = re.sub(r'^\d+\.\s+', '', q_text) # Remove "1. "
            
            opts = [m.group(2).strip(), m.group(3).strip(), m.group(4).strip(), m.group(5).strip()]
            
            mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            if ans_char in mapping:
                correct = opts[mapping[ans_char]]
                
                Question.objects.create(
                    test=test,
                    text=q_text,
                    options=opts,
                    correct_answer=correct,
                    category="Maths",
                    type="mcq"
                )
                count += 1
            else:
                 print(f"Invalid Answer Char: {ans_char} for Q: {q_text[:20]}")
        else:
            print(f"Failed to match options in block: {block[:50]}...")

    print(f"Successfully added {count} questions.")

if __name__ == '__main__':
    parse_and_add()
