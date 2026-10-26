<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * Tabel sales_orders — header order penjualan
     */
    public function up(): void
    {
        Schema::create('sales_orders', function (Blueprint $table) {
            $table->id();
            $table->string('order_number', 30)->unique()->comment('Nomor order unik, contoh: SO-2026-0001');
            $table->foreignId('customer_id')
                  ->constrained('customers')
                  ->restrictOnDelete()
                  ->comment('Relasi ke tabel customers');
            $table->date('order_date')->comment('Tanggal order dibuat');
            $table->enum('status', [
                'DRAFT',
                'SUBMITTED',
                'APPROVED',
                'DELIVERED',
                'INVOICED',
                'PAID',
                'CANCELLED',
            ])->default('DRAFT')->comment('Status alur order penjualan');
            $table->text('notes')->nullable()->comment('Catatan tambahan order');
            $table->timestamps();
            $table->softDeletes();

            // Index untuk filter dan laporan
            $table->index('customer_id');
            $table->index('order_date');
            $table->index('status');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('sales_orders');
    }
};
