#!/usr/bin/env python
"""
this module need easy_logging
"""
import os
import pandas as pd
import numpy as np
from easy_logging.easylogging import EasyVerboseLogging

EVLobj = EasyVerboseLogging()
EVLobj.set_class_logger_level('INFO')
EVLobj.get_class_logger()


class HitZombieRoad(object):

    def __init__(self):
        self.logger = EasyVerboseLogging().get_class_logger()
        self.black_dice = None
        self.red_dice = None
        self._set_dice()
        self.human_nums = None
        self.normal_zombie_nums = None
        self.elite_zombie_nums = None
        self._set_default_value()
        self.df_result_info = None
        self.df_statistics_info = None
        self._reset_df()
        self.small_round = 1
        self.test_loop = 1

    def _set_dice(self):
        self.black_dice = {
            1: ["kill"],
            2: ["nothing"],
            3: ["kill"],
            4: ["death", "adrenaline"],
            5: ["adrenaline"],
            6: ["kill", "adrenaline"]}

        self.red_dice = {
            1: ["kill"],
            2: ["death"],
            3: ["kill"],
            4: ["death", "adrenaline"],
            5: ["adrenaline"],
            6: ["kill", "adrenaline"]}

    def _set_default_value(self):
        self.human_nums = 5
        self.normal_zombie_nums = 4
        self.elite_zombie_nums = 2

    def _reset_df(self):
        self.df_result_info = pd.DataFrame(
            columns=['human_nums',
                     'normal_zombie_nums',
                     'elite_zombie_nums',
                     'result_round_num',
                     'result_death',
                     'win_or_lose'])

        self.df_result_info_with_adrenaline = pd.DataFrame(
            columns=['human_nums',
                     'normal_zombie_nums',
                     'elite_zombie_nums',
                     'result_round_num',
                     'adrenaline_use',
                     'result_death',
                     'win_or_lose'])

        self.df_statistics_info = pd.DataFrame(
            columns=['human_nums',
                     'normal_zombie_nums',
                     'elite_zombie_nums',
                     'winning_probability',
                     'death_mean',
                     'round_mean',
                     'experiment_times'])
        
        self.df_statistics_info_with_adrenaline = pd.DataFrame(
            columns=['human_nums',
                     'normal_zombie_nums',
                     'elite_zombie_nums',
                     'winning_probability',
                     'death_mean',
                     'adrenaline_mean',
                     'round_mean',
                     'experiment_times']
        )        
        

    def _get_dice_number(self, current_human_nums, current_normal_zombie_nums, current_elite_zombie_nums):
        this_round_red_dice_nums = min(current_human_nums, current_elite_zombie_nums)
        this_round_black_dice_nums = current_human_nums - this_round_red_dice_nums
        self.logger.debug(f'Round:{self.small_round}, '
                          f'Human:{current_human_nums}, '
                          f'Normal Zombie:{current_normal_zombie_nums}, '
                          f'Elite Zombie:{current_elite_zombie_nums}, '
                          f'Red Dice:{this_round_red_dice_nums}, '
                          f'Black Dice:{this_round_black_dice_nums}')
        return this_round_black_dice_nums, this_round_red_dice_nums

    def _get_dice_result(self, black_dice_nums, red_dice_nums):
        red_dice_result = np.random.randint(1, 7, red_dice_nums)
        black_dice_result = np.random.randint(1, 7, black_dice_nums)

        round_dice_result = []
        for item in red_dice_result:
            round_dice_result.append(self.red_dice[int(item)])

        for item in black_dice_result:
            round_dice_result.append(self.black_dice[int(item)])

        self.logger.debug(f'Round:{self.small_round}, '
                          f'Red Dice Num:{red_dice_result}, '
                          f'Black Dice Num:{black_dice_result}, '
                          f'Total Result:{round_dice_result}')
        return round_dice_result

    def fuck_zombie_with_adrenaline(self):
        current_normal_zombie_nums = self.normal_zombie_nums
        current_elite_zombie_nums = self.elite_zombie_nums
        current_human_nums = self.human_nums
        win_or_lose_flag = None
        if current_normal_zombie_nums + current_elite_zombie_nums > 0:
            pass
        else:
            self.logger.debug(f'No Zombie Exist, '
                              f'Normal = {current_normal_zombie_nums}, '
                              f'Elite = {current_elite_zombie_nums}')

        adrenaline_numbers = 0
        while True:
            death_numbers = 0            
            if (current_normal_zombie_nums + current_elite_zombie_nums > 0) and (current_human_nums > 0):
                zombie_nums_in_this_round = current_normal_zombie_nums + current_elite_zombie_nums
                black_dice_nums, red_dice_nums = self._get_dice_number(
                    current_human_nums=current_human_nums,
                    current_normal_zombie_nums=current_normal_zombie_nums,
                    current_elite_zombie_nums=current_elite_zombie_nums)

                round_dice_result = self._get_dice_result(
                    black_dice_nums=black_dice_nums,
                    red_dice_nums=red_dice_nums)                

                for result_list in round_dice_result:
                    if 'kill' in result_list:
                        if current_normal_zombie_nums > 0:
                            current_normal_zombie_nums = current_normal_zombie_nums - 1
                            if current_normal_zombie_nums < 0:
                                current_normal_zombie_nums = 0
                        elif current_normal_zombie_nums == 0 and current_elite_zombie_nums > 0:
                            current_elite_zombie_nums = current_elite_zombie_nums - 1
                            if current_elite_zombie_nums < 0:
                                current_elite_zombie_nums = 0

                    if 'death' in result_list:
                        if 'adrenaline' in result_list:
                            adrenaline_numbers = adrenaline_numbers + 1
                        else:
                            if current_human_nums > 0:
                                current_human_nums = current_human_nums - 1

                death_numbers = self.human_nums - current_human_nums
                self.logger.debug(
                    f'Round:{self.small_round}, '
                    f'Total Zombie:{zombie_nums_in_this_round}, '
                    f'Normal Zombie:{current_normal_zombie_nums}, '
                    f'Elite Zombie:{current_elite_zombie_nums}, '
                    f'Adrenaline:{adrenaline_numbers}, '
                    f'Human Alive:{current_human_nums}, '
                    f'Human Death:{death_numbers}')
                if (current_normal_zombie_nums + current_elite_zombie_nums == 0) or (current_human_nums == 0):
                    if current_human_nums > 0:
                        self.logger.debug(f'Human Win!')
                        win_or_lose_flag = 'win'
                    else:
                        self.logger.debug(f'Human Lose!')
                        win_or_lose_flag = 'lose'
                    break

            else:
                self.logger.error(f'Some Error Happened!')
                break

            self.small_round = self.small_round + 1

            if self.small_round >= 100:
                break

        result_dict = {'human_nums': [self.human_nums],
                       'normal_zombie_nums': [self.normal_zombie_nums],
                       'elite_zombie_nums': [self.elite_zombie_nums],
                       'result_round_num': [self.small_round],
                       'adrenaline_use': [adrenaline_numbers],
                       'result_death': [death_numbers],
                       'win_or_lose': [win_or_lose_flag]}
        self.small_round = 1
        return result_dict


    def fuck_zombie_without_resource(self):
        current_normal_zombie_nums = self.normal_zombie_nums
        current_elite_zombie_nums = self.elite_zombie_nums
        current_human_nums = self.human_nums
        win_or_lose_flag = None
        if current_normal_zombie_nums + current_elite_zombie_nums > 0:
            pass
        else:
            self.logger.debug(f'No Zombie Exist, '
                              f'Normal = {current_normal_zombie_nums}, '
                              f'Elite = {current_elite_zombie_nums}')

        while True:
            death_numbers = 0
            if (current_normal_zombie_nums + current_elite_zombie_nums > 0) and (current_human_nums > 0):
                zombie_nums_in_this_round = current_normal_zombie_nums + current_elite_zombie_nums
                black_dice_nums, red_dice_nums = self._get_dice_number(
                    current_human_nums=current_human_nums,
                    current_normal_zombie_nums=current_normal_zombie_nums,
                    current_elite_zombie_nums=current_elite_zombie_nums)

                round_dice_result = self._get_dice_result(
                    black_dice_nums=black_dice_nums,
                    red_dice_nums=red_dice_nums)                

                for result_list in round_dice_result:
                    if 'kill' in result_list:
                        if current_normal_zombie_nums > 0:
                            current_normal_zombie_nums = current_normal_zombie_nums - 1
                            if current_normal_zombie_nums < 0:
                                current_normal_zombie_nums = 0
                        elif current_normal_zombie_nums == 0 and current_elite_zombie_nums > 0:
                            current_elite_zombie_nums = current_elite_zombie_nums - 1
                            if current_elite_zombie_nums < 0:
                                current_elite_zombie_nums = 0

                    if 'death' in result_list:
                        if current_human_nums > 0:
                            current_human_nums = current_human_nums - 1

                death_numbers = self.human_nums - current_human_nums
                self.logger.debug(
                    f'Round:{self.small_round}, '
                    f'Total Zombie:{zombie_nums_in_this_round}, '
                    f'Normal Zombie:{current_normal_zombie_nums}, '
                    f'Elite Zombie:{current_elite_zombie_nums}, '
                    f'Human Alive:{current_human_nums}, '
                    f'Human Death:{death_numbers}')
                if (current_normal_zombie_nums + current_elite_zombie_nums == 0) or (current_human_nums == 0):
                    if current_human_nums > 0:
                        self.logger.debug(f'Human Win!')
                        win_or_lose_flag = 'win'
                    else:
                        self.logger.debug(f'Human Lose!')
                        win_or_lose_flag = 'lose'
                    break

            else:
                self.logger.error(f'Some Error Happened!')
                break

            self.small_round = self.small_round + 1

            if self.small_round >= 100:
                break

        result_dict = {'human_nums': [self.human_nums],
                       'normal_zombie_nums': [self.normal_zombie_nums],
                       'elite_zombie_nums': [self.elite_zombie_nums],
                       'result_round_num': [self.small_round],
                       'result_death': [death_numbers],
                       'win_or_lose': [win_or_lose_flag]}
        self.small_round = 1
        return result_dict

    def set_para(self, human, normal_zombie, elite_zombie):
        self.human_nums = human
        self.normal_zombie_nums = normal_zombie
        self.elite_zombie_nums = elite_zombie

    def simulate_for_no_resource(self, loop_max=1000):
        for human in range(1, 11):
            for normal in range(0, 11):
                for elite in range(0, 5):
                    print(normal,elite)
                    if normal + elite > 0:
                        print(f'Zombies:{normal + elite}')
                    else:
                        self.logger.debug(f'No Zombies:normal={normal},elite={elite}')
                        continue

                    if os.path.exists(f'result/human_{human}_normal_{normal}_elite_{elite}.csv'):
                        self.df_result_info = pd.read_csv(
                            f'result/human_{human}_normal_{normal}_elite_{elite}.csv',
                            index_col=0)
                    else:
                        self.df_result_info = pd.DataFrame(
                            columns=['human_nums',
                                     'normal_zombie_nums',
                                     'elite_zombie_nums',
                                     'result_round_num',
                                     'result_death',
                                     'win_or_lose'])
                        

                    if os.path.exists(f'result/statistics_info.csv'):
                        self.df_statistics_info = pd.read_csv(
                            f'result/statistics_info.csv',
                            index_col=0)
                    else:
                        self.df_statistics_info = pd.DataFrame(
                            columns=['human_nums',
                                     'normal_zombie_nums',
                                     'elite_zombie_nums',
                                     'winning_probability',
                                     'death_mean',
                                     'round_mean',
                                     'experiment_times'])

                    for test_loop in range(0, loop_max):
                        self.logger.info(f'------------------------test_loop:{test_loop}------------------------')
                        self.set_para(human, normal, elite)
                        result_dict = self.fuck_zombie_without_resource()
                        self.logger.info(f'result={result_dict}')
                        if len(self.df_result_info) >= 11111:
                            break
                        self.df_result_info = self.df_result_info.append(
                            pd.DataFrame(result_dict), ignore_index=True, sort=False)

                    self.df_result_info.to_csv(f'result/human_{human}_normal_{normal}_elite_{elite}.csv')
                    self.logger.info(f'Save Success: result/human_{human}_normal_{normal}_elite_{elite}.csv')

                    round_mean = self.df_result_info['result_round_num'].mean()
                    death_mean = self.df_result_info['result_death'].mean()
                    winning_probability = (
                            len(self.df_result_info[self.df_result_info['win_or_lose'] == 'win']) /
                            len(self.df_result_info) * 100)

                    statistics_dict = {'human_nums': [human],
                                       'normal_zombie_nums': [normal],
                                       'elite_zombie_nums': [elite],
                                       'winning_probability': [winning_probability],
                                       'death_mean': [death_mean],
                                       'round_mean': [round_mean],
                                       'experiment_times': [len(self.df_result_info)]}

                    _drop_index_list = list(
                        self.df_statistics_info[
                            (self.df_statistics_info['human_nums'] == human) &
                            (self.df_statistics_info['normal_zombie_nums'] == normal) &
                            (self.df_statistics_info['elite_zombie_nums'] == elite)].index)

                    if len(_drop_index_list) > 0:
                        self.df_statistics_info = self.df_statistics_info.drop(index=_drop_index_list)

                    self.df_statistics_info = self.df_statistics_info.append(
                        pd.DataFrame(statistics_dict), ignore_index=True, sort=False)

                    self.df_statistics_info.to_csv(f'result/statistics_info.csv')
                    self.logger.info(f'result/statistics_info.csv')


    def simulate_with_adrenaline(self, loop_max=1000):
        for human in range(1, 11):
            for normal in range(0, 11):
                for elite in range(0, 6):
                    print(normal,elite)
                    if normal + elite > 0:
                        print(f'Zombies:{normal + elite}')
                    else:
                        self.logger.debug(f'No Zombies:normal={normal},elite={elite}')
                        continue

                    if os.path.exists(f'result_with_adrenaline/human_{human}_normal_{normal}_elite_{elite}.csv'):
                        self.df_result_info_with_adrenaline = pd.read_csv(
                            f'result_with_adrenaline/human_{human}_normal_{normal}_elite_{elite}.csv',
                            index_col=0)
                    else:
                        self.df_result_info_with_adrenaline = pd.DataFrame(
                            columns=['human_nums',
                                     'normal_zombie_nums',
                                     'elite_zombie_nums',
                                     'result_round_num',
                                     'adrenaline_use',
                                     'result_death',
                                     'win_or_lose'])

                    if os.path.exists(f'result_with_adrenaline/statistics_info.csv'):
                        self.df_statistics_info_with_adrenaline = pd.read_csv(
                            f'result_with_adrenaline/statistics_info.csv',
                            index_col=0)
                    else:
                        self.df_statistics_info_with_adrenaline = pd.DataFrame(
                            columns=['human_nums',
                                     'normal_zombie_nums',
                                     'elite_zombie_nums',
                                     'winning_probability',
                                     'death_mean',
                                     'adrenaline_mean',
                                     'round_mean',
                                     'experiment_times'])

                    for test_loop in range(0, loop_max):
                        self.logger.info(f'------------------------test_loop:{test_loop}------------------------')
                        self.set_para(human, normal, elite)
                        result_dict = self.fuck_zombie_with_adrenaline()
                        self.logger.info(f'result={result_dict}')
                        if len(self.df_result_info_with_adrenaline) >= 10000:
                            break
                        self.df_result_info_with_adrenaline = self.df_result_info_with_adrenaline.append(
                            pd.DataFrame(result_dict), ignore_index=True, sort=False)

                    self.df_result_info_with_adrenaline.to_csv(f'result_with_adrenaline/human_{human}_normal_{normal}_elite_{elite}.csv')
                    self.logger.info(f'Save Success: result_with_adrenaline/human_{human}_normal_{normal}_elite_{elite}.csv')

                    round_mean = self.df_result_info_with_adrenaline['result_round_num'].mean()
                    death_mean = self.df_result_info_with_adrenaline['result_death'].mean()
                    adrenaline_mean = self.df_result_info_with_adrenaline['adrenaline_use'].mean()
                    winning_probability = (
                            len(self.df_result_info_with_adrenaline[self.df_result_info_with_adrenaline['win_or_lose'] == 'win']) /
                            len(self.df_result_info_with_adrenaline) * 100)

                    statistics_dict = {'human_nums': [human],
                                       'normal_zombie_nums': [normal],
                                       'elite_zombie_nums': [elite],
                                       'winning_probability': [winning_probability],
                                       'death_mean': [death_mean],
                                       'adrenaline_mean': [adrenaline_mean],
                                       'round_mean': [round_mean],
                                       'experiment_times': [len(self.df_result_info_with_adrenaline)]}

                    _drop_index_list = list(
                        self.df_statistics_info_with_adrenaline[
                            (self.df_statistics_info_with_adrenaline['human_nums'] == human) &
                            (self.df_statistics_info_with_adrenaline['normal_zombie_nums'] == normal) &
                            (self.df_statistics_info_with_adrenaline['elite_zombie_nums'] == elite)].index)

                    if len(_drop_index_list) > 0:
                        self.df_statistics_info_with_adrenaline = self.df_statistics_info_with_adrenaline.drop(index=_drop_index_list)

                    self.df_statistics_info_with_adrenaline = self.df_statistics_info_with_adrenaline.append(
                        pd.DataFrame(statistics_dict), ignore_index=True, sort=False)

                    self.df_statistics_info_with_adrenaline.to_csv(f'result_with_adrenaline/statistics_info.csv')
                    self.logger.info(f'result_with_adrenaline/statistics_info.csv')






if __name__ == '__main__':
    HZRobj = HitZombieRoad()
    while True:
        HZRobj.simulate_with_adrenaline(100)
    # for i in range(0,100):
    #     HZRobj.set_para(100,1000,100)
    #     print(HZRobj.fuck_zombie_with_adrenaline())