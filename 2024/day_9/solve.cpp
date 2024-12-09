#include <fstream>
#include <iostream>
#include <chrono>
#include <vector>

void calculate_checksum_for_individual_movement(std::vector<int> numbers, const size_t number_of_blocks);
void calculate_checksum_for_block_movement(std::vector<int> numbers, const size_t number_of_blocks);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <file_path>" << std::endl;
        return 1;
    }

    std::ifstream file(argv[1]);
    std::string input;
    getline(file, input);
    file.close();

    std::vector<int> numbers;
    numbers.reserve(input.length());
    size_t number_of_blocks = 0;
    for (auto index = 0; index < input.size(); ++index)
    {
        numbers.push_back(input[index] - '0');
        if (index % 2 == 0)
        {
            number_of_blocks += numbers[index];
        }
    }
    std::chrono::high_resolution_clock timer;
    auto start = timer.now();
    calculate_checksum_for_individual_movement(numbers, number_of_blocks);
    auto end = timer.now();
    std::cout << "The first part took " << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << " microseconds" << std::endl;

    start = timer.now();
    calculate_checksum_for_block_movement(numbers, number_of_blocks);
    end = timer.now();
    std::cout << "The second part took " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " milliseconds" << std::endl;

    return 0;
}

void calculate_checksum_for_individual_movement(std::vector<int> numbers, const size_t number_of_blocks)
{
    size_t checksum = 0;
    size_t file_index = 0;
    size_t copy_index = numbers.size() - 1; // indicates the file for which the content is copied
    for(auto memory_index = 0; memory_index < number_of_blocks;)
    {
        size_t length_of_block;
        size_t value_in_block;
        if (file_index %2 == 0)
        {
            length_of_block = numbers[file_index];
            value_in_block = file_index/2;
            ++file_index;
        }
        else
        {
            length_of_block = std::min(numbers[file_index], numbers[copy_index]);
            value_in_block = copy_index/2;
            numbers[file_index] -= length_of_block;
            numbers[copy_index] -= length_of_block;
            if (numbers[file_index] == 0)
            {
                ++file_index;
            }
            if (numbers[copy_index] == 0)
            {
                copy_index-=2;
            }
        }
        checksum += (2 * memory_index + length_of_block - 1) * length_of_block * value_in_block / 2;
        memory_index += length_of_block;
    }
    std::cout << "The checksum for the first part is " << checksum << std::endl;
}

void calculate_checksum_for_block_movement(std::vector<int> numbers, const size_t number_of_blocks)
{
    const auto original_numbers = numbers;
    size_t checksum = 0;
    size_t file_index = 0;
    size_t copy_index = numbers.size() - 1; // indicates the file for which the content is copied
    for(auto memory_index = 0; file_index < numbers.size();)
    {
        size_t length_of_block;
        size_t value_in_block;
        if (file_index %2 == 0)
        {
            if (numbers[file_index] == 0)
            {
                memory_index += original_numbers[file_index];
                ++file_index;
                continue;
            }
            length_of_block = numbers[file_index];
            numbers[file_index] = 0;
            value_in_block = file_index/2;
            ++file_index;
        }
        else
        {
            if (copy_index <= 0)
            {
                copy_index = numbers.size() - 1;
                memory_index += numbers[file_index];
                ++file_index;
                continue;
            }
            if (numbers[file_index] >= numbers[copy_index] && numbers[copy_index] != 0)
            {
                length_of_block = numbers[copy_index];
                value_in_block = copy_index/2;
                numbers[file_index] -= length_of_block;
                numbers[copy_index] = 0;
                copy_index=numbers.size()-1;
            }
            else
            {
                copy_index-=2;
                continue;
            }
            if (numbers[file_index] == 0)
            {
                ++file_index;
            }
        }
        if(value_in_block != 0)
        {
            checksum += (2 * memory_index + length_of_block - 1) * length_of_block * value_in_block / 2;
        }
        memory_index += length_of_block;
    }
    std::cout << "The checksum for the second part is " << checksum << std::endl;
}