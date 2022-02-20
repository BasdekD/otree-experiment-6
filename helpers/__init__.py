from otree.api import *
import logging
import random


# Real effort task initialization
def get_random_tables(C):
    random_tables = random.sample(C.TABLES, C.NUM_OF_TABLES)
    tables = list()
    for table in random_tables:
        tables.append(table['table'])
    answers = list()
    for table in random_tables:
        answers.append(int(table['zeros']))
    return tables, answers


# Player handling
def get_dropout_timeout(player, timeout):
    participant = player.participant
    if participant.is_dropout:
        return 1
    else:
        return timeout


def dropout_handler_before_next_page(player, timeout_happened):
    participant = player.participant
    if timeout_happened:
        player.number_of_consecutive_timeout_pages += 1
    else:
        player.number_of_consecutive_timeout_pages = 0
    if player.number_of_consecutive_timeout_pages >= player.session.config['max_cons_timeout_pages']:
        participant.is_dropout = True


def dropout_handler_app_after_this_page(player, upcoming_apps):
    if player.participant.is_dropout:
        return upcoming_apps[-1]
    else:
        pass


# Comprehension Question Handling
def question_final_income_get_answer_index(player):
    return [2] if player.session.config['efficacy'] == 'high' else [4]


def question_final_income_get_answer(player):
    return 2 if player.session.config['efficacy'] == 'high' else 1


# Player grouping
def get_redundant_players(subsession, waiting_players):
    redundant_players = list()
    for player in filter(lambda p: p not in waiting_players, subsession.get_players()):
        redundant_players.append(player)
        player.participant.is_overbooked = True
    return redundant_players


def set_initial_group_matrix(subsession, waiting_players, redundant_players):
    import random
    random.shuffle(waiting_players)
    subsession.set_group_matrix([
        [player.id_in_subsession for player in waiting_players],
        [player.id_in_subsession for player in redundant_players]
    ])


def set_groups(subsession, C):
    waiting_players = list()
    for player in filter(lambda p: p.participant.has_reached_main is True, subsession.get_players()):
        if len(waiting_players) < C.PLAYERS_PER_GROUP:
            waiting_players.append(player)
    redundant_players = get_redundant_players(subsession, waiting_players)
    set_initial_group_matrix(subsession, waiting_players, redundant_players)


# Income handling based on contributions
def calculate_total_public_pool(subsession):
    total_public_pool_ap = 0
    dropouts = []
    for player in subsession.get_groups()[0].get_players():
        if not player.timeout_on_contribution:
            total_public_pool_ap += player.public_pool_ap
        else:
            dropouts.append(player)
    non_dropout_number = len(subsession.get_players()) - len(dropouts)
    if non_dropout_number == 0:
        return 0
    for _ in dropouts:
        total_public_pool_ap += int(total_public_pool_ap / non_dropout_number)
    return total_public_pool_ap


def convert_exchange_ap_to_income(subsession):
    for player in subsession.get_groups()[0].get_players():
        player.payoff += cu(player.exchange_ap * subsession.session.config['ap_to_money_cu'])
        logging.info('Exchange income: {}'.format(player.payoff))


def adjust_payrates(subsession):
    total_public_pool_ap = calculate_total_public_pool(subsession)
    if subsession.session.config['efficacy'] == 'high':
        if total_public_pool_ap <= 11:
            pass
        elif 12 <= total_public_pool_ap <= 23:
            subsession.final_low_income = cu(2)
            subsession.final_high_income = cu(4)
        elif 24 <= total_public_pool_ap:
            subsession.final_low_income = cu(3)
            subsession.final_high_income = cu(3)
    else:
        if total_public_pool_ap <= 27:
            pass
        elif 28 <= total_public_pool_ap <= 39:
            subsession.final_low_income = cu(2)
            subsession.final_high_income = cu(4)
        elif total_public_pool_ap == 40:
            subsession.final_low_income = cu(3)
            subsession.final_high_income = cu(3)


def switch_groups(subsession):
    players = subsession.get_players()
    players.sort(key=lambda e: e.personal_account_ap)
    players[-1].has_switched = True
    players[-2].has_switched = True
