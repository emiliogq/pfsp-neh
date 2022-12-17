from matplotlib import pyplot as plt
from matplotlib import transforms
from neh import read_instance_file, neh
from solution import Solution

def make_plotting_data(problems, starting_instance):
    gaps, elapsed_times, names = [], [], []
    for problem in problems:
        problem_file, problem_bsk = problem
        jobs, machines = read_instance_file(problem_file)
        solution:Solution
        solution, elapsed_time = neh(jobs, machines)
        gap_percent = (abs(solution.makespan - problem_bsk) / (problem_bsk * 0.01))
        names.append("Taillard "+str(starting_instance))
        gaps.append(gap_percent)
        elapsed_times.append(elapsed_time)
        starting_instance += 1
    return gaps, names, elapsed_times

def test_neh():

    jobs, machines = read_instance_file("data/tai117_500_20_inputs.txt")
    solution:Solution
    solution, elapsed_time = neh(jobs, machines)
    assert solution.makespan == solution.calculate_makespan()
    assert str(solution) == "(464 444 312 112 326 320 461 237 278 438 5 113 17 93 472 234 140 7 247 390 310 462 447 115 500 477 22 194 405 265 360 352 416 241 473 295 141 260 228 102 62 182 454 203 117 216 176 238 388 459 422 426 145 236 242 475 142 303 156 133 458 57 493 324 162 379 68 222 26 178 290 254 54 397 187 196 8 263 27 445 104 151 495 398 20 321 448 31 395 270 378 144 85 19 111 308 243 106 300 48 421 232 150 430 307 212 97 412 91 296 316 256 52 47 36 173 337 43 277 252 209 128 471 64 70 3 118 69 184 269 336 407 44 197 335 149 334 257 155 239 455 344 218 13 166 325 135 351 488 264 482 110 330 153 280 2 481 146 478 304 224 148 214 391 371 485 127 109 443 169 431 119 322 491 180 86 191 370 350 432 114 25 328 451 480 12 78 460 116 136 287 249 9 341 342 367 332 490 206 33 193 408 139 401 457 134 105 393 11 359 55 452 159 275 221 442 208 425 50 483 286 185 383 74 71 179 470 233 217 72 289 189 170 15 309 372 409 271 355 107 392 299 319 177 49 449 188 175 125 181 440 333 51 101 463 126 220 172 419 429 67 100 198 499 137 361 37 219 281 171 362 225 292 30 387 120 314 158 272 399 250 411 386 192 268 414 143 329 130 246 29 424 215 384 200 211 376 132 89 349 415 294 131 365 389 285 40 183 434 99 301 400 327 366 186 273 418 10 428 474 380 92 59 466 446 164 245 41 279 498 402 439 129 124 199 291 262 435 204 357 258 356 152 14 235 468 274 24 167 311 201 317 413 302 354 331 288 87 255 229 293 66 369 346 79 230 53 476 147 297 486 467 261 373 63 417 207 347 1 318 343 38 108 94 77 35 18 32 90 437 420 494 340 65 284 453 163 487 95 348 174 339 338 394 404 305 61 381 484 375 227 456 253 441 266 450 46 75 492 58 160 76 202 83 403 39 60 240 23 56 81 323 489 82 28 313 4 123 496 226 353 315 406 42 382 465 368 374 248 21 436 34 165 154 157 73 98 364 396 358 276 45 223 282 377 433 168 423 103 84 267 306 283 138 497 231 122 205 410 161 6 259 121 427 469 479 80 16 298 190 96 195 251 213 345 385 210 88 363 244)"

def test_neh_performance():

    # Data file, BSK, solution
    # http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/flowshop.dir/best_lb_up.txt
    small_sized_problems = [ 
        ("data/tai001_20_5_inputs.txt", 1278),
        ("data/tai002_20_5_inputs.txt", 1359),
        ("data/tai003_20_5_inputs.txt", 1081),
        ("data/tai004_20_5_inputs.txt", 1293),
        ("data/tai005_20_5_inputs.txt", 1235),
        ("data/tai006_20_5_inputs.txt", 1195),
        ("data/tai007_20_5_inputs.txt", 1234),
        ("data/tai008_20_5_inputs.txt", 1206),
        ("data/tai009_20_5_inputs.txt", 1230),
        ("data/tai010_20_5_inputs.txt", 1108),
    ]
    
    medium_sized_problems = [ 
        ("data/tai091_200_10_inputs.txt", 10862),
        ("data/tai092_200_10_inputs.txt", 10480),
        ("data/tai093_200_10_inputs.txt", 10922),
        ("data/tai094_200_10_inputs.txt", 10889),
        ("data/tai095_200_10_inputs.txt", 10524),
        ("data/tai096_200_10_inputs.txt", 10329),
        ("data/tai097_200_10_inputs.txt", 10854),
        ("data/tai098_200_10_inputs.txt", 10730),
        ("data/tai099_200_10_inputs.txt", 10438),
        ("data/tai100_200_10_inputs.txt", 10675),
    ]

    big_sized_problems = [ 
        ("data/tai111_500_20_inputs.txt", 26040),
        ("data/tai112_500_20_inputs.txt", 26500),
        ("data/tai113_500_20_inputs.txt", 26371),
        ("data/tai114_500_20_inputs.txt", 26456),
        ("data/tai115_500_20_inputs.txt", 26334),
        ("data/tai116_500_20_inputs.txt", 26469),
        ("data/tai117_500_20_inputs.txt", 26389),
        ("data/tai118_500_20_inputs.txt", 26560),
        ("data/tai119_500_20_inputs.txt", 26005),
        ("data/tai120_500_20_inputs.txt", 26457),
    ]

    problems = [
        (small_sized_problems,"NEH performance with small-sized instances (20x5)", 1), 
        (medium_sized_problems, "NEH performance with medium-sized instances (200x10)", 91),
        (big_sized_problems, "NEH performance with big-sized instances (500x20)", 111)
    ]
    i = 0
    figure, axes = plt.subplots(len(problems), 1)
    figure.tight_layout(pad=1.0)
    for problem_size in problems:
        files, title, starting_instance = problem_size
        gaps, instance_names, elapsed_times =  make_plotting_data(files, starting_instance)
        axes[i].plot(instance_names, gaps)
        avg_gaps, avg_eta = sum(gaps) / len(gaps), sum(elapsed_times) / len(elapsed_times)
        axes[i].axhline(avg_gaps)
        axes[i].set_title(title)
        axes[i].set_ylabel("Gap percent")
        axes[i].set_xlabel("Taillard instances")
        axes[i].text(0,avg_gaps, "{:.2f}".format(avg_gaps), color="red", ha="right")
        i += 1  

    plt.show()