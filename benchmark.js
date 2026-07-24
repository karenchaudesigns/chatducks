const fs = require('fs');

// We will mock activeUsers and the args.
const numUsers = 10000;
const numArgs = 100;

const activeUsers = new Map();
for (let i = 0; i < numUsers; i++) {
    activeUsers.set(`User${i}`, { isLurking: false, isStatic: false, isBusy: false, name: `User${i}` });
}

const args = [];
for (let i = 0; i < numArgs; i++) {
    args.push(`@user${i * 100}`);
}

function testOriginal() {
    let participants = new Set();
    const start = performance.now();
    for (let arg of args) {
        let targetName = arg.startsWith('@') ? arg.substring(1) : arg;
        let targetUser = null;
        for (let [k, v] of activeUsers.entries()) {
            if (k.toLowerCase() === targetName.toLowerCase()) {
                targetUser = v;
                break;
            }
        }
        if (targetUser && !targetUser.isLurking && !targetUser.isStatic && !targetUser.isBusy) {
            participants.add(targetUser);
        }
    }
    const end = performance.now();
    return end - start;
}

function testOptimized() {
    let participants = new Set();
    const start = performance.now();

    let lowerCaseActiveUsers = null;

    for (let arg of args) {
        let targetName = arg.startsWith('@') ? arg.substring(1) : arg;
        let targetUser = activeUsers.get(targetName);

        if (!targetUser) {
            if (!lowerCaseActiveUsers) {
                lowerCaseActiveUsers = new Map();
                for (let [k, v] of activeUsers.entries()) {
                    lowerCaseActiveUsers.set(k.toLowerCase(), v);
                }
            }
            targetUser = lowerCaseActiveUsers.get(targetName.toLowerCase());
        }

        if (targetUser && !targetUser.isLurking && !targetUser.isStatic && !targetUser.isBusy) {
            participants.add(targetUser);
        }
    }
    const end = performance.now();
    return end - start;
}

let sumOriginal = 0;
let sumOptimized = 0;
const iterations = 100;

// warmup
testOriginal();
testOptimized();

for (let i = 0; i < iterations; i++) {
    sumOriginal += testOriginal();
    sumOptimized += testOptimized();
}

console.log(`Original Avg: ${sumOriginal / iterations} ms`);
console.log(`Optimized Avg: ${sumOptimized / iterations} ms`);
