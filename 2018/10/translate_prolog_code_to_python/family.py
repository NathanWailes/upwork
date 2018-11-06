from collections import defaultdict

males = set()
males.add('Joe')
males.add('Bill')
males.add('Paul')
males.add('Mike')
males.add('Adam')

females = set()
females.add('Marie')
females.add('Helen')
females.add('Miranda')

parents_of = defaultdict(set)
parents_of['Joe'].add('Helen')
parents_of['Joe'].add('Bill')
parents_of['Marie'].add('Helen')
parents_of['Marie'].add('Bill')
parents_of['Bill'].add('Mike')
parents_of['Helen'].add('Adam')
parents_of['Paul'].add('Miranda')
parents_of['Miranda'].add('Mike')


def male(person):
    return person in males


def female(person):
    return person in females


def parent_of(person_1, person_2):
    return person_2 in parents_of[person_1]


def sibling_of(person_1, person_2):
    return bool(person_1 != person_2 and parents_of[person_1].intersection(parents_of[person_2]))


def brother_of(person_1, person_2):
    return sibling_of(person_1, person_2) and person_2 in males


def sister_of(person_1, person_2):
    return sibling_of(person_1, person_2) and person_2 in females


def mother_of(person_1, person_2):
    return person_2 in parents_of[person_1] and person_2 in females


def father_of(person_1, person_2):
    return person_2 in parents_of[person_1] and person_2 in males


def gp_of(person_1, person_2):
    for parent_of_person_1 in parents_of[person_1]:
        grandparents = parents_of[parent_of_person_1]
        if person_2 in grandparents:
            return True
    return False


def grandparents_of(person):
    grandparents = set()
    for parent in parents_of[person]:
        grandparents = grandparents.union(parents_of[parent])
    return grandparents


def cousin_of(person_1, person_2):
    if person_1 == person_2 or sibling_of(person_1, person_2):
        return False

    if grandparents_of(person_1).intersection(grandparents_of(person_2)):
        return True


if __name__ == '__main__':
    assert sibling_of('Joe', 'Marie')
    assert sibling_of('Marie', 'Joe')

    assert brother_of('Marie', 'Joe')
    assert sister_of('Joe', 'Marie')

    assert mother_of('Joe', 'Helen')
    assert father_of('Joe', 'Bill')

    assert gp_of('Joe', 'Mike')
    assert gp_of('Joe', 'Mike')

    assert cousin_of('Joe', 'Paul')
    assert cousin_of('Marie', 'Paul')
