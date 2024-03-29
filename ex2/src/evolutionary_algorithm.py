import random 

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.hill_climbing import * 
from src.load_solution import loadAndParseSolution



def generateSolutions(solutions, evals):
    newSolutions = []
    newSolutionsChanges = []
    newSolutionsEvaluation = []

    for i in range(0, len(solutions)):
        newSolutions.append(solutions[i])
        newSolutionsChanges.append([])
        newSolutionsEvaluation.append(evals[i])

    # Crossover
    for i in range(0,len(solutions)):
        for j in range(0, len(solutions)):
            if (i == j):
                next
            
            newSolution = cloneSolutions(solutions[i][0])
            newSolutionChanges = []

            # Accept 0.05 - 0.2 percent of another solution
            lower = random.uniform(0,0.8)
            upper = random.uniform(lower+0.05,lower+0.2)

            lowerIndex = int(lower * len(solutions[i][0]))
            upperIndex = int(upper * len(solutions[i][0]))

            if lowerIndex == upperIndex:
                next

            for k in range(lowerIndex, upperIndex):
                newSolutionChanges.append((newSolution[0][k][0], newSolution[0][k][1], solutions[j][0][k][2].getX() - newSolution[0][k][2].getX()))
                newSolution[0][k][2].setX(solutions[j][0][k][2].getX())

            newSolutions.append(newSolution)
            newSolutionsChanges.append(newSolutionChanges)
            newSolutionsEvaluation.append(evals[i])

    # Mutation

    for i in range(0, len(solutions)):
        percentage = random.uniform(0.01,0.05)

        newSolution = cloneSolutions(solutions[i][0])
        newSolutionChanges = []

        lower = random.uniform(0,1 - percentage)
        upper = lower + percentage

        lowerIndex = int(lower * len(solutions[i][0]))
        upperIndex = int(upper * len(solutions[i][0]))

        if lowerIndex == upperIndex:
            if upperIndex < (len(solutions[i][0]) - 1):
                upperIndex = upperIndex + 1
            else:
                lowerIndex = lowerIndex - 1

        for k in range(lowerIndex, upperIndex):
            newValue = random.randint(0,1)
            newSolutionChanges.append((newSolution[0][k][0], newSolution[0][k][1], newValue - newSolution[0][k][2].getX()))
            newSolution[0][k][2].setX(newValue)

        newSolutions.append(newSolution)
        newSolutionsChanges.append(newSolutionChanges)
        newSolutionsEvaluation.append(evals[i])
    
    if len(solutions[0][0]) > 100:
        for i in range(0, len(solutions)):

            newSolution = cloneSolutions(solutions[i][0])
            newSolutionChanges = []

            fixedRandom = min(len(newSolution[0]), random.randint(4,6))
            if fixedRandom % 2 == 1:
                fixedRandom = fixedRandom - 1
            
            fixedStart = random.randint(0,len(newSolution[0]) - fixedRandom)
        
            #print(str(fixedStart))

            for j in range(fixedStart, fixedRandom + fixedStart, 2):
                costj = newSolution[0][j][2].singleCost()
                costj1 = newSolution[0][j+1][2].singleCost()

                if (costj < costj1):
                    newSolutionChanges.append((newSolution[0][j][0], newSolution[0][j][1], 1  - newSolution[0][j][2].getX()))
                    newSolutionChanges.append((newSolution[0][j+1][0], newSolution[0][j+1][1], 0  - newSolution[0][j][2].getX()))

                    newSolution[0][j][2].setX(1)
                    newSolution[0][j+1][2].setX(0)
                else:
                    newSolutionChanges.append((newSolution[0][j][0], newSolution[0][j][1], 0  - newSolution[0][j][2].getX()))
                    newSolutionChanges.append((newSolution[0][j+1][0], newSolution[0][j+1][1], 1  - newSolution[0][j][2].getX()))

                    newSolution[0][j][2].setX(0)
                    newSolution[0][j+1][2].setX(1)

            newSolutions.append(newSolution)
            newSolutionsChanges.append(newSolutionChanges)
            newSolutionsEvaluation.append(evals[i])

    #print('S' + str(len(newSolutions)) + '::' + str(len(newSolutionsChanges)) + '::' + str(len(newSolutionsEvaluation)))

    return (newSolutions, newSolutionsChanges, newSolutionsEvaluation)

def evaluateSolutions(newSols, verticesD, avgCs3Cost):
    newSolutions = newSols[0]
    newSolutionsChanges = newSols[1]
    newSolutionsEvaluation = newSols[2]

    result = []

    for i in range(0, len(newSolutions)):
        curCost = iterativeCost(newSolutions[i][1], newSolutions[i][0], verticesD, newSolutionsEvaluation[i], newSolutionsChanges[i], avgCs3Cost)

        result.append((curCost, newSolutions[i]))

    return result

def evolutionaryAlgorithm(inits,
        graph,
        maxIter = 100,
        populationSize = 5,
        maxTime = 60,
        startTime = -1,
        traceMode = False,
        verbose = True):

    # Generate Initial Solutions
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits

    solutions = []
    evaluations = []

    trace = []

    if (graph[2] is not None):
        # If specified add the solution
        sol = loadAndParseSolution(graph[2], directedEdges)
        (solL, solD) = sol
        solutions.append(sol)
        evaluations.append(completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict))

    for i in range(0, populationSize):
        #sol = initSolutions(inits[0])
        #randomizedInit(sol[0])
        
        #(solL, solD) = sol
        (solL, solD) = initGreedySolutions(inits, graph)

        solCost =  completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
        # Infeasible for larger solutions
        # (solD, solL, solCost) = hillClimber(graph, inits, sol)
        repair(solD, solL, solCost, inits, graph)
        solutions.append((solL, solD))
        evaluations.append(solCost)

    greedySol = initGreedySolutions(inits, graph)
    solutions.append(greedySol)
    greedyCost = completeCost(greedySol[1], greedySol[0], graph[0], directedEdges, costDict, pathDict)
    evaluations.append(greedyCost)

    zeroSol = initSolutions(inits[0])

    oneSol = initSolutions(inits[0])
    validInit(oneSol[0])

    zeroSolEvaluation = completeCost(zeroSol[1], zeroSol[0], graph[0], directedEdges, costDict, pathDict)
    oneSolEvaluation = completeCost(oneSol[1], oneSol[0], graph[0], directedEdges, costDict, pathDict)

    curBestSol = cloneSolutions(greedySol[0])
    curBestEvaluation = greedyCost

    curTmpBestSol = cloneSolutions(greedySol[0])
    curTmpBestEvaluation = greedyCost


    if startTime == -1:
        startTime = time.time()

    for i in range(0, maxIter):
        if not isInTime(startTime, maxTime):
            break
        
        # -------------------------------MORE-RANDOM-START-----------------
        # These interchanges may lead to better results (more random)
        #clonedZero = cloneSolutions(zeroSol[0])
        #clonedOne = cloneSolutions(oneSol[0])
        if (i+1) % 15 == 0:
            clonedBest = cloneSolutions(curBestSol[0])

        #solutions.append(clonedZero)
        #solutions.append(clonedOne)
        if (i+1) % 15 == 0:
            solutions.append(clonedBest)

        #evaluations.append(zeroSolEvaluation)
        #evaluations.append(oneSolEvaluation)
        if (i+1) % 15 == 0:
            evaluations.append(curBestEvaluation)
        # -------------------------------MORE-RANDOM-END-----------------
        newSols = generateSolutions(solutions, evaluations)
        
        solEvals = evaluateSolutions(newSols, verticesD, avgPerViolation)

        # --------------------------------MOVE-ACCEPT-------------------
        solEvals.sort(key = lambda x: x[0][0][3])

        solutions = []
        evaluations = []

        for j in range(0, populationSize):
            solutions.append(solEvals[j][1])
            evaluations.append(solEvals[j][0])

        if traceMode:
            trace.append(evaluations[0])

        if (i+1) % 10 == 0:
            # Every few iterations recalculate the cost exactly
            evaluations = []
            if verbose:
                print('<<<Iteration ' + str(i))
            for j in range(0, populationSize):
                sol = solutions[j]
                cost = completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict)
                if (cost[0][3] < curBestEvaluation[0][3]):
                    curBestSol = cloneSolutions(sol[0])
                    curBestEvaluation = cost

                evaluations.append(cost)
                if verbose:
                    print('    Accepted with cost ' + str(cost[0][3]))
    
            if verbose:
                print('>>>')
           
       
        # Works quite good for small examples, but too inefficient for larger ones
 
        """
        converged = True
        for j in range(1, populationSize):
            if (evaluations[j][0][3] != evaluations[j-1][0][3]):
                converged = False
                break

        if converged == True:
            (solD, solL, solCost) = hillClimber(graph, inits, solutions[0])
            repair(solD, solL, solCost, inits, graph)
            solCost = (completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict))

            solutions[0] = (solL, solD)
            evaluations[0] = solCost

            for j in range(1, populationSize):
                sol = initSolutions(inits[0])
                randomizedInit(sol[0])
                solutions[j] = (sol)
                evaluations[j] = (completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict))
        """
    
    if traceMode:
        trace.append(curBestEvaluation)
        return (curBestSol, solutions, trace)
    else:
        return (curBestSol, solutions)

