from brain.core.brain import AIBrain

brain = AIBrain()

question = input("Ask AI Brain: ")

answer = brain.answer(question)

print("\n====================")
print("AI Brain Answer")
print("====================")
print(answer)